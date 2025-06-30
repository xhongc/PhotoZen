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
        total_favorites = Photo.objects.filter(favorited_by=self.context.request.user).count()
        
        # 计算总存储空间（字节）
        total_storage = Photo.objects.aggregate(total_size=Sum('size'))['total_size'] or 0
        
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