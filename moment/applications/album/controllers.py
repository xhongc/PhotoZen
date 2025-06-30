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

from applications.photos.models import Photo
from .models import Album
from .schema import (
    AlbumSchema,
    AlbumCreateSchema,
    AlbumUpdateSchema,
    BulkAddPhotosSchema,
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