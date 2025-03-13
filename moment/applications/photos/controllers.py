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
    @route.get(
        "",
        response=PaginatedResponseSchema[PhotoSchema],
        url_name="photos",
    )
    @paginate(PageNumberPaginationExtra)
    def list(
        self,
        time_filter: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        location: Optional[str] = None,
        favorites_only: bool = False,
        sort_by: str = "-upload_time",
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
            now = timezone.now()
            if time_filter == "30days":
                queryset = queryset.filter(upload_time__gte=now - timedelta(days=30))
            elif time_filter == "90days":
                queryset = queryset.filter(upload_time__gte=now - timedelta(days=90))
            elif time_filter == "1year":
                queryset = queryset.filter(upload_time__gte=now - timedelta(days=365))
        elif start_date and end_date:
            queryset = queryset.filter(upload_time__range=[start_date, end_date])

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
        if sort_by == "oldest":
            queryset = queryset.order_by("upload_time")
        elif sort_by == "newest":
            queryset = queryset.order_by("-upload_time")
        elif sort_by == "rating":
            queryset = queryset.order_by("-rating")

        return queryset

    @route.post(
        "",
        response=PhotoSchema,
        url_name="upload-photo"
    )
    def upload(self, data: PhotoUploadSchema, file: File):
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
