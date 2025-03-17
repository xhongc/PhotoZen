from applications.photos.schema import (
    PhotoSchema, PhotoUploadSchema, PhotoUpdateSchema,
    PhotoRatingSchema, LocationSchema
)
from django.contrib.auth import get_user_model
from ninja_extra import ControllerBase
from ninja_extra import api_controller, route
from ninja_extra.pagination import (
    PageNumberPaginationExtra,
    PaginatedResponseSchema,
    paginate,
)
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from django.utils import timezone
from datetime import datetime, timedelta
from typing import Optional, List
from django.db.models import Q, Exists, OuterRef
from django.shortcuts import get_object_or_404
from django.core.files import File
from PIL import Image
import io
import os

from .models import Photo, Tag, Location, PhotoRating

User = get_user_model()


@api_controller("/photos", auth=JWTAuth(), permissions=[IsAuthenticated])
class PhotoController(ControllerBase):
    model_config = {
        "arbitrary_types_allowed": True
    }

    @route.get(
        "",
        response=list[dict],
        url_name="photos",
    )
    def list(
        self,
        time_filter: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        location: Optional[str] = None,
        favorites_only: bool = False,
        sort_by: str = "-taken_time",
        group_by: str = "day",
        page: int = 1,
        page_size: int = 20
    ):
        # 添加用户收藏状态的子查询
        favorites_subquery = User.objects.filter(
            favorite_photos=OuterRef('pk'),
            id=self.context.request.user.id
        )

        queryset = Photo.objects.annotate(
            is_favorite=Exists(favorites_subquery)
        )

        # 时间筛选
        if time_filter:
            time_filter = datetime.strptime(time_filter, "%Y-%m-%d")
            start_date = time_filter - timedelta(days=30)
            end_date = time_filter + timedelta(days=30)
            queryset = queryset.filter(
                taken_time__range=[start_date, end_date])
        elif start_date and end_date:
            queryset = queryset.filter(
                taken_time__range=[start_date, end_date])
        
        # 标签筛选
        if tags:
            tag_query = Q()
            for tag in tags:
                tag_query |= Q(tags__name=tag)
            queryset = queryset.filter(tag_query).distinct()

        # 位置筛选
        if location:
            queryset = queryset.filter(location__name__icontains=location)

        # 收藏筛选
        if favorites_only:
            queryset = queryset.filter(favorited_by=self.context.request.user)

        # 排序
        queryset = queryset.order_by(sort_by)
        queryset = queryset[page_size * (page - 1):page_size * page]
        # 按天分组
        result = {}
        if group_by == "day":
            for photo in queryset:
                date_key = photo.taken_time.date().isoformat()
                if date_key not in result:
                    result[date_key] = []
                result[date_key].append(photo)
        elif group_by == "month":
            for photo in queryset:
                date_key = photo.taken_time.strftime("%Y-%m")
                if date_key not in result:
                    result[date_key] = []
                result[date_key].append(photo)
        res = []
        for key, value in result.items():
            res.append({
                "date_key": key,
                "photos": [PhotoSchema.from_orm(photo).dict() for photo in value]
            })
        return res

    @route.post(
        "",
        response=PhotoSchema,
        url_name="upload-photo"
    )
    def upload(self, data: PhotoUploadSchema):
        # 从请求中获取文件
        file = self.context.request.FILES.get('photo')
        if not file:
            raise ValueError("No photo file provided")

        # 处理图片文件
        img = Image.open(file)
        width, height = img.size

        # 创建缩略图
        thumbnail_size = (300, 300)
        img.thumbnail(thumbnail_size)
        thumb_io = io.BytesIO()
        img.save(thumb_io, format=img.format)

        # 创建或获取位置信息
        location = None
        if data.location:
            location, _ = Location.objects.get_or_create(
                latitude=data.location.latitude,
                longitude=data.location.longitude,
                defaults={'name': data.location.name}
            )

        # 创建照片记录
        photo = Photo.objects.create(
            title=data.title,
            description=data.description or "",
            taken_time=data.taken_time,
            location=location,
            file_path=file,
            size=file.size,
            width=width,
            height=height,
            format=img.format
        )

        # 处理标签
        if data.tags:
            for tag_name in data.tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                photo.tags.add(tag)

        return photo

    @route.put(
        "/{photo_id}",
        response=PhotoSchema,
        url_name="update-photo"
    )
    def update(self, photo_id: int, data: PhotoUpdateSchema):
        photo = self.get_object_or_404(Photo, id=photo_id)

        # 更新基本信息
        if data.title is not None:
            photo.title = data.title
        if data.description is not None:
            photo.description = data.description
        if data.taken_time is not None:
            photo.taken_time = data.taken_time

        # 更新位置信息
        if data.location:
            location, _ = Location.objects.get_or_create(
                latitude=data.location.latitude,
                longitude=data.location.longitude,
                defaults={'name': data.location.name}
            )
            photo.location = location

        # 更新标签
        if data.tags is not None:
            photo.tags.clear()
            for tag_name in data.tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                photo.tags.add(tag)

        photo.save()
        return photo

    @route.delete(
        "/{photo_id}",
        url_name="delete-photo"
    )
    def delete(self, photo_id: int):
        photo = self.get_object_or_404(Photo, id=photo_id)
        photo.delete()
        return {"success": True}

    @route.post(
        "/{photo_id}/rate",
        response=PhotoSchema,
        url_name="rate-photo"
    )
    def rate(self, photo_id: int, data: PhotoRatingSchema):
        photo = self.get_object_or_404(Photo, id=photo_id)

        # 创建或更新评分
        rating, created = PhotoRating.objects.get_or_create(
            photo=photo,
            user=self.context.request.user,
            defaults={
                'rating': data.rating,
                'comment': data.comment or ""
            }
        )

        if not created:
            rating.rating = data.rating
            rating.comment = data.comment or ""
            rating.save()

        # 更新照片的平均评分
        photo.update_rating(data.rating)
        return photo

    @route.post(
        "/{photo_id}/favorite",
        response=PhotoSchema,
        url_name="favorite-photo"
    )
    def toggle_favorite(self, photo_id: int):
        photo = self.get_object_or_404(Photo, id=photo_id)
        user = self.context.request.user

        if user in photo.favorited_by.all():
            photo.favorited_by.remove(user)
        else:
            photo.favorited_by.add(user)

        return photo

    @route.get(
        "/{photo_id}",
        response=PhotoSchema,
        url_name="photo-detail"
    )
    def get_photo(self, photo_id: int):
        photo = self.get_object_or_404(Photo, id=photo_id)
        return photo

    @route.get(
        "/tags",
        response=List[str],
        url_name="photo-tags"
    )
    def get_tags(self):
        return Tag.objects.values_list("name", flat=True)
