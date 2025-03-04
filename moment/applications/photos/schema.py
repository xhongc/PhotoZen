from datetime import datetime
from typing import List

from django.contrib.auth import get_user_model
from ninja_schema import Schema

UserModel = get_user_model()


# Schemas
class TagSchema(Schema):
    id: int
    name: str


class AlbumSchema(Schema):
    id: int
    name: str
    description: str
    created_time: datetime
    updated_time: datetime


class PhotoSchema(Schema):
    id: int
    title: str
    description: str
    file_path: str
    thumbnail_path: str
    upload_time: datetime
    taken_time: datetime = None
    size: int
    width: int
    height: int
    format: str
    albums: List[AlbumSchema]
    tags: List[TagSchema]