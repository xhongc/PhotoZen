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
from typing import List

from applications.photos.models import Photo
from .models import Album
from .schema import (
    AlbumSchema,
    AlbumCreateSchema,
    AlbumUpdateSchema,
    BulkAddPhotosSchema,
    SystemAlbumSchema,
    PhotoSchema,
)

User = get_user_model()

@api_controller("/albums", auth=JWTAuth(), permissions=[IsAuthenticated])
class AlbumController(ControllerBase):
    @route.get(
        "",
        response=PaginatedResponseSchema[AlbumSchema],
        url_name="albums"
    )
    @paginate(PageNumberPaginationExtra)
    def list(self):
        """获取当前用户的所有相册列表"""
        return Album.objects.filter()

    @route.post(
        "",
        response=AlbumSchema,
        url_name="create-album"
    )
    def create(self, data: AlbumCreateSchema):
        """创建新相册"""
        album = Album.objects.create(
            name=data.name,
            description=data.description or "",
            owner=self.context.request.user
        )
        return album

    @route.get(
        "/{album_id}",
        response=AlbumSchema,
        url_name="album-detail"
    )
    def get_album(self, album_id: int):
        """获取相册详情"""
        return get_object_or_404(
            Album,
            id=album_id,
            owner=self.context.request.user
        )

    @route.put(
        "/{album_id}",
        response=AlbumSchema,
        url_name="update-album"
    )
    def update(self, album_id: int, data: AlbumUpdateSchema):
        """更新相册信息"""
        album = get_object_or_404(
            Album,
            id=album_id,
            owner=self.context.request.user
        )
        
        album.name = data.name
        album.description = data.description or ""
        
        if data.cover_photo_id:
            cover_photo = get_object_or_404(
                Photo,
                id=data.cover_photo_id,
                albums=album
            )
            album.cover_photo = cover_photo
            
        album.save()
        return album

    @route.delete(
        "/{album_id}",
        url_name="delete-album"
    )
    def delete(self, album_id: int):
        """删除相册"""
        album = get_object_or_404(
            Album,
            id=album_id,
            owner=self.context.request.user
        )
        album.delete()
        return {"success": True}

    @route.post(
        "/{album_id}/photos/bulk",
        response=AlbumSchema,
        url_name="bulk-add-photos-to-album"
    )
    def bulk_add_photos(self, album_id: int, data: BulkAddPhotosSchema):
        """批量添加照片到相册"""
        album = get_object_or_404(
            Album,
            id=album_id,
        )
        
        # 获取所有照片
        photos = Photo.objects.filter(id__in=data.photo_ids)
        
        # 批量添加照片
        album.photos.add(*photos)
        
        # 如果相册没有封面，将第一张照片设为封面
        if not album.cover_photo and photos.exists():
            album.cover_photo = photos.first()
            album.save()
            
        return album

    @route.get(
        "/{album_id}/photos",
        response=PaginatedResponseSchema[PhotoSchema],
        url_name="album-photos"
    )
    @paginate(PageNumberPaginationExtra)
    def get_photos(self, album_id: int):
        """获取相册中的照片"""
        album = get_object_or_404(
            Album,
            id=album_id,
            owner=self.context.request.user
        )
        return album.photos.all().order_by('-taken_time')

    @route.delete(
        "/{album_id}/photos/{photo_id}",
        response=AlbumSchema,
        url_name="remove-photo-from-album"
    )
    def remove_photo(self, album_id: int, photo_id: int):
        """从相册中移除照片"""
        album = get_object_or_404(
            Album,
            id=album_id,
            owner=self.context.request.user
        )
        photo = get_object_or_404(Photo, id=photo_id)
        
        album.photos.remove(photo)
        
        # 如果移除的是封面照片，更新封面
        if album.cover_photo == photo:
            new_cover = album.photos.first()
            album.cover_photo = new_cover
            album.save()
            
        return album

@api_controller("/favorite", auth=JWTAuth(), permissions=[IsAuthenticated])
class FavoriteController(ControllerBase):
    @route.post(
        "/photos/bulk",
        response=dict,
        url_name="bulk-add-photos-to-favorite"
    )
    def bulk_add_favorite(self, data: BulkAddPhotosSchema):
        """批量添加照片到收藏相册"""
        album = get_object_or_404(
            Album,
            name="收藏"
        )
        
        # 获取所有照片
        photos = Photo.objects.filter(id__in=data.photo_ids)
        
        # 批量添加照片
        album.photos.add(*photos)
        
        # 如果相册没有封面，将第一张照片设为封面
        if not album.cover_photo and photos.exists():
            album.cover_photo = photos.first()
        album.save()
            
        return {"success": True} 

@api_controller("/system-albums", auth=JWTAuth(), permissions=[IsAuthenticated])
class SystemAlbumController(ControllerBase):
    @route.get(
        "",
        response=List[SystemAlbumSchema],
        url_name="system-albums"
    )
    def list(self):
        """获取系统相册统计信息"""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Q
        
        def create_cover_photo(photo):
            if photo:
                return {
                    'id': photo.id,
                    'url': photo.file_path.url if photo.file_path else '',
                    'title': photo.title
                }
            return None
        
        # 最近添加 - 最近30天的照片
        recent_cutoff = timezone.now() - timedelta(days=30)
        recent_photos = Photo.objects.filter(taken_time__gte=recent_cutoff).order_by('-taken_time')
        recent_count = recent_photos.count()
        recent_cover = recent_photos.first()
        
        # 收藏 - 名为"收藏"的相册中的照片
        try:
            favorite_album = Album.objects.get(name="收藏")
            favorite_count = favorite_album.photos_count
            favorite_cover = favorite_album.cover_photo
        except Album.DoesNotExist:
            favorite_count = 0
            favorite_cover = None
        
        # 截图 - 根据文件名判断是否为截图
        screenshot_photos = Photo.objects.filter(
            Q(title__icontains='screenshot') | 
            Q(title__icontains='截图') |
            Q(title__icontains='屏幕快照') |
            Q(file_path__icontains='screenshot') |
            Q(file_path__icontains='Screen Shot')
        ).order_by('-taken_time')
        screenshot_count = screenshot_photos.count()
        screenshot_cover = screenshot_photos.first()
        
        # 自拍 - 这里可以扩展为人脸识别功能，暂时返回部分照片作为示例
        selfie_photos = Photo.objects.filter(
            Q(title__icontains='selfie') | 
            Q(title__icontains='自拍') |
            Q(file_path__icontains='selfie')
        ).order_by('-taken_time')
        selfie_count = selfie_photos.count()
        selfie_cover = selfie_photos.first()
        
        # 视频 - 根据文件扩展名判断
        video_photos = Photo.objects.filter(
            Q(file_path__iendswith='.mp4') |
            Q(file_path__iendswith='.mov') |
            Q(file_path__iendswith='.avi') |
            Q(file_path__iendswith='.mkv') |
            Q(file_path__iendswith='.wmv') |
            Q(file_path__iendswith='.m4v')
        ).order_by('-taken_time')
        video_count = video_photos.count()
        video_cover = video_photos.first()
        
        # 人物 - 这里可以扩展为人脸识别功能，暂时返回所有照片的一部分
        people_photos = Photo.objects.all().order_by('-taken_time')
        people_count = people_photos.count() 
        people_cover = people_photos.first()
        
        # 地点 - 这里可以扩展为GPS位置功能，暂时返回所有照片的一部分
        places_photos = Photo.objects.all().order_by('-taken_time')
        places_count = places_photos.count()
        places_cover = places_photos.first()
        
        # 今年 - 今年拍摄的照片
        current_year = timezone.now().year
        this_year_photos = Photo.objects.filter(taken_time__year=current_year).order_by('-taken_time')
        this_year_count = this_year_photos.count()
        this_year_cover = this_year_photos.first()
        
        return [
            {
                'name': '最近添加',
                'photos_count': recent_count,
                'cover_photo': create_cover_photo(recent_cover),
                'type': 'recent'
            },
            {
                'name': '收藏',
                'photos_count': favorite_count,
                'cover_photo': create_cover_photo(favorite_cover),
                'type': 'favorite'
            },
            {
                'name': '今年',
                'photos_count': this_year_count,
                'cover_photo': create_cover_photo(this_year_cover),
                'type': 'this_year'
            },
            {
                'name': '截图',
                'photos_count': screenshot_count,
                'cover_photo': create_cover_photo(screenshot_cover),
                'type': 'screenshots'
            },
            {
                'name': '自拍',
                'photos_count': selfie_count,
                'cover_photo': create_cover_photo(selfie_cover),
                'type': 'selfies'
            },
            {
                'name': '视频',
                'photos_count': video_count,
                'cover_photo': create_cover_photo(video_cover),
                'type': 'videos'
            },
            {
                'name': '人物',
                'photos_count': people_count,
                'cover_photo': create_cover_photo(people_cover),
                'type': 'people'
            },
            {
                'name': '地点',
                'photos_count': places_count,
                'cover_photo': create_cover_photo(places_cover),
                'type': 'places'
            }
        ]

    @route.get(
        "/{album_type}/photos",
        response=PaginatedResponseSchema[PhotoSchema],
        url_name="system-album-photos"
    )
    @paginate(PageNumberPaginationExtra)
    def get_system_album_photos(self, album_type: str):
        """获取系统相册中的照片"""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Q
        
        if album_type == 'recent':
            recent_cutoff = timezone.now() - timedelta(days=30)
            photos = Photo.objects.filter(taken_time__gte=recent_cutoff).order_by('-taken_time')
        elif album_type == 'favorite':
            try:
                favorite_album = Album.objects.get(name="收藏")
                photos = favorite_album.photos.all().order_by('-taken_time')
            except Album.DoesNotExist:
                photos = Photo.objects.none()
        elif album_type == 'this_year':
            current_year = timezone.now().year
            photos = Photo.objects.filter(taken_time__year=current_year).order_by('-taken_time')
        elif album_type == 'screenshots':
            photos = Photo.objects.filter(
                Q(title__icontains='screenshot') | 
                Q(title__icontains='截图') |
                Q(title__icontains='屏幕快照') |
                Q(file_path__icontains='screenshot') |
                Q(file_path__icontains='Screen Shot')
            ).order_by('-taken_time')
        elif album_type == 'selfies':
            photos = Photo.objects.filter(
                Q(title__icontains='selfie') | 
                Q(title__icontains='自拍') |
                Q(file_path__icontains='selfie')
            ).order_by('-taken_time')
        elif album_type == 'videos':
            photos = Photo.objects.filter(
                Q(file_path__iendswith='.mp4') |
                Q(file_path__iendswith='.mov') |
                Q(file_path__iendswith='.avi') |
                Q(file_path__iendswith='.mkv') |
                Q(file_path__iendswith='.wmv') |
                Q(file_path__iendswith='.m4v')
            ).order_by('-taken_time')
        elif album_type == 'people':
            photos = Photo.objects.all().order_by('-taken_time')
        elif album_type == 'places':
            photos = Photo.objects.all().order_by('-taken_time')
        else:
            photos = Photo.objects.none()
            
        return photos