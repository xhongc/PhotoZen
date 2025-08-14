from django.conf import settings
from applications.photos.schema import (
    PhotoSchema, PhotoUploadSchema, PhotoUpdateSchema,
    PhotoRatingSchema, LocationSchema
)
from applications.photos.metadata_schema import (
    PhotoMetadataSchema, ExifDataSchema, CustomFieldCreateSchema,
    CustomFieldUpdateSchema, ExifFieldUpdateSchema, GPSCoordinatesSchema,
    CameraInfoSchema, ShootingParametersSchema, MetadataResponseSchema,
    PhotoMetadataDetailSchema
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
from django.http import FileResponse
from django.core.exceptions import ValidationError
from PIL import Image
import io
import os

from .models import Photo, Tag, Location, PhotoRating, PhotoMetadata
from .metadata import PhotoMetadataEditor

User = get_user_model()


@api_controller("/photos", auth=JWTAuth(), permissions=[IsAuthenticated])
class PhotoController(ControllerBase):
    model_config = {
        "arbitrary_types_allowed": True
    }

    @route.get(
        "",
        response=List[dict],
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
        page_size: int = 20,
        album_id: Optional[int] = None
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
        if album_id:
            queryset = queryset.filter(albums=album_id)
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
        elif group_by == "item":
            return [
                {
                    "date_key": "item",
                    "photos": [PhotoSchema.from_orm(photo).dict() for photo in queryset]
                }
            ]

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
        photo = get_object_or_404(Photo, id=photo_id)

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
        photo = get_object_or_404(Photo, id=photo_id)
        photo.delete()
        return {"success": True}

    @route.post(
        "/{photo_id}/rate",
        response=PhotoSchema,
        url_name="rate-photo"
    )
    def rate(self, photo_id: int, data: PhotoRatingSchema):
        photo = get_object_or_404(Photo, id=photo_id)

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
        photo = get_object_or_404(Photo, id=photo_id)
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
        photo = get_object_or_404(Photo, id=photo_id)
        return photo

    @route.get(
        "/tags",
        response=List[str],
        url_name="photo-tags"
    )
    def get_tags(self):
        return Tag.objects.values_list("name", flat=True)

    @route.get(
        "/{photo_id}/file",
        url_name="photo-file"
    )
    def get_photo_file(self, photo_id: int):
        photo = get_object_or_404(Photo, id=photo_id)
        
        # 检查文件是否存在
        if not photo.file_path:
            raise ValueError("照片文件未找到")
        real_path = photo.file_path.path.replace(str(settings.MEDIA_ROOT), settings.PHOTO_FOLDER_PREFIX)

        # 打开文件并读取为二进制流
        with open(real_path, 'rb') as f:
            file_data = f.read()
            
        # 创建内存中的文件流
        file_stream = io.BytesIO(file_data)
        
        # 返回文件流响应
        return FileResponse(
            file_stream,
            content_type=f"image/{photo.format.lower()}",
            filename=os.path.basename(real_path)
        )

    # === 元数据相关 API ===
    @route.get(
        "/{photo_id}/metadata",
        response=PhotoMetadataSchema,
        url_name="photo-metadata"
    )
    def get_metadata(self, photo_id: int):
        """获取照片的完整元数据"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            metadata = editor.get_metadata()
            return metadata
        except Exception as e:
            raise ValidationError(f"获取元数据失败: {str(e)}")
    
    @route.get(
        "/{photo_id}/metadata/exif",
        response=ExifDataSchema,
        url_name="photo-exif-data"
    )
    def get_exif_data(self, photo_id: int):
        """仅获取EXIF数据"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            exif_data = editor.get_exif_data()
            return {"data": exif_data}
        except Exception as e:
            raise ValidationError(f"获取EXIF数据失败: {str(e)}")
    
    @route.put(
        "/{photo_id}/metadata/exif",
        response=MetadataResponseSchema,
        url_name="update-exif-field"
    )
    def update_exif_field(self, photo_id: int, data: ExifFieldUpdateSchema):
        """更新EXIF字段"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            success = editor.update_exif_field(data.tag, data.value)
            return {
                "success": success,
                "message": f"EXIF字段 '{data.tag}' 更新成功" if success else "更新失败"
            }
        except ValidationError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"更新EXIF字段失败: {str(e)}"
            }
    
    @route.post(
        "/{photo_id}/metadata/custom",
        response=PhotoMetadataDetailSchema,
        url_name="add-custom-field"
    )
    def add_custom_field(self, photo_id: int, data: CustomFieldCreateSchema):
        """添加自定义元数据字段"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            metadata = editor.add_custom_field(
                key=data.key,
                name=data.name,
                value=data.value,
                field_type=data.field_type
            )
            return metadata
        except ValidationError as e:
            raise ValidationError(str(e))
        except Exception as e:
            raise ValidationError(f"添加自定义字段失败: {str(e)}")
    
    @route.put(
        "/{photo_id}/metadata/custom/{field_key}",
        response=MetadataResponseSchema,
        url_name="update-custom-field"
    )
    def update_custom_field(self, photo_id: int, field_key: str, data: CustomFieldUpdateSchema):
        """更新自定义元数据字段"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            success = editor.update_custom_field(field_key, data.value)
            return {
                "success": success,
                "message": f"自定义字段 '{field_key}' 更新成功" if success else "更新失败"
            }
        except ValidationError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"更新自定义字段失败: {str(e)}"
            }
    
    @route.delete(
        "/{photo_id}/metadata/custom/{field_key}",
        response=MetadataResponseSchema,
        url_name="delete-custom-field"
    )
    def delete_custom_field(self, photo_id: int, field_key: str):
        """删除自定义元数据字段"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            success = editor.remove_custom_field(field_key)
            return {
                "success": success,
                "message": f"自定义字段 '{field_key}' 删除成功" if success else "删除失败"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"删除自定义字段失败: {str(e)}"
            }
    
    @route.get(
        "/{photo_id}/metadata/gps",
        response=Optional[GPSCoordinatesSchema],
        url_name="photo-gps-coordinates"
    )
    def get_gps_coordinates(self, photo_id: int):
        """获取照片GPS坐标"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            coordinates = editor.get_gps_coordinates()
            if coordinates:
                return {
                    "latitude": coordinates[0],
                    "longitude": coordinates[1]
                }
            return None
        except Exception as e:
            raise ValidationError(f"获取GPS坐标失败: {str(e)}")
    
    @route.get(
        "/{photo_id}/metadata/camera",
        response=CameraInfoSchema,
        url_name="photo-camera-info"
    )
    def get_camera_info(self, photo_id: int):
        """获取相机信息"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            camera_info = editor.get_camera_info()
            return camera_info
        except Exception as e:
            raise ValidationError(f"获取相机信息失败: {str(e)}")
    
    @route.get(
        "/{photo_id}/metadata/shooting",
        response=ShootingParametersSchema,
        url_name="photo-shooting-parameters"
    )
    def get_shooting_parameters(self, photo_id: int):
        """获取拍摄参数"""
        photo = get_object_or_404(Photo, id=photo_id)
        editor = PhotoMetadataEditor(photo)
        
        try:
            shooting_params = editor.get_shooting_parameters()
            return shooting_params
        except Exception as e:
            raise ValidationError(f"获取拍摄参数失败: {str(e)}")
    
    @route.get(
        "/{photo_id}/metadata/custom",
        response=List[PhotoMetadataDetailSchema],
        url_name="photo-custom-fields"
    )
    def get_custom_fields(self, photo_id: int):
        """获取所有自定义字段"""
        photo = get_object_or_404(Photo, id=photo_id)
        custom_fields = photo.custom_metadata.all()
        return list(custom_fields)
