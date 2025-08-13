from django.contrib.auth import get_user_model
from ninja_extra import ControllerBase, api_controller, route
from ninja_extra.pagination import (
    PageNumberPaginationExtra,
    PaginatedResponseSchema,
    paginate,
)
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone

from applications.photos.models import Photo
from applications.album.models import Album

User = get_user_model()


@api_controller("/home", auth=JWTAuth(), permissions=[IsAuthenticated])
class HomeController(ControllerBase):
    @route.get(
        "/",
        response=dict,
        url_name="home"
    )
    def home(self):
        """首页"""
        # 获取统计信息
        total_photos = Photo.objects.count()
        total_albums = Album.objects.count()
        total_favorites = Photo.objects.filter(
            favorited_by=self.context.request.user).count()

        # 计算总存储空间（字节）
        total_storage = Photo.objects.aggregate(
            total_size=Sum('size'))['total_size'] or 0

        # 转换存储空间为更友好的格式
        storage_units = ['B', 'KB', 'MB', 'GB', 'TB']
        storage_size = total_storage
        unit_index = 0

        while storage_size >= 1024 and unit_index < len(storage_units) - 1:
            storage_size /= 1024
            unit_index += 1

        formatted_storage = f"{storage_size:.2f} {storage_units[unit_index]}"

        return {
            "total_photos": total_photos,
            "total_albums": total_albums,
            "total_favorites": total_favorites,
            "storage_space": formatted_storage,
            "success": True
        }

    @route.get(
        "/memories",
        response=dict,
        url_name="today_memories"
    )
    def today_memories(self):
        """今日回忆 - 获取往年今日拍摄的照片"""
        today = timezone.now().date()
        current_year = today.year

        # 查找往年今日拍摄的照片（排除今年）
        memories = []
        for years_ago in range(1, 6):  # 查找过去5年
            target_year = current_year - years_ago
            target_date_start = datetime(
                target_year, today.month, today.day, 0, 0, 0)
            target_date_end = datetime(
                target_year, today.month, today.day, 23, 59, 59)

            # todo mock
            target_date_start = datetime(2022, 9, 11, 0, 0, 0)
            target_date_end = datetime(2022, 9, 11, 23, 59, 59)

            photos = Photo.objects.filter(
                taken_time__range=(target_date_start, target_date_end)
            ).order_by('-taken_time')[:6]  # 每年最多取6张

            if photos.exists():
                photo_list = self._format_photos_for_memories(photos)
                memory_data = self._create_memory_data(target_year, years_ago, photo_list)
                memories.append(memory_data)

        return {
            "memories": memories,
            "success": True
        }

    def _format_photos_for_memories(self, photos):
        """格式化照片数据用于回忆展示"""
        photo_list = []
        for photo in photos:
            formatted_photo = {
                "id": photo.id,
                "title": photo.title,
                "thumbnail_path": self._get_photo_thumbnail_url(photo),
                "taken_time": photo.taken_time.strftime('%Y-%m-%d %H:%M'),
                "description": photo.description
            }
            photo_list.append(formatted_photo)
        return photo_list

    def _get_photo_thumbnail_url(self, photo):
        """获取照片缩略图URL"""
        base_url = "http://127.0.0.1:8000"
        if photo.thumbnail_path:
            return base_url + photo.thumbnail_path.url
        else:
            return base_url + photo.file_path.url

    def _create_memory_data(self, target_year, years_ago, photo_list):
        """创建回忆数据结构"""
        return {
            "year": target_year,
            "years_ago": years_ago,
            "photos": photo_list
        }
