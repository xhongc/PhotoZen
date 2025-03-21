from ninja import Schema
from datetime import datetime
from typing import Optional, List

class AlbumPhotoSchema(Schema):
    id: int
    url: str
    title: Optional[str] = None

class AlbumBaseSchema(Schema):
    name: str
    description: Optional[str] = None

class AlbumCreateSchema(AlbumBaseSchema):
    pass

class AlbumUpdateSchema(AlbumBaseSchema):
    cover_photo_id: Optional[int] = None

class AlbumSchema(AlbumBaseSchema):
    id: int
    created_time: datetime
    updated_time: datetime
    photos_count: int
    cover_photo: Optional[AlbumPhotoSchema] = None

class BulkAddPhotosSchema(Schema):
    photo_ids: List[int] 