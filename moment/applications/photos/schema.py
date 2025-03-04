from datetime import datetime
from typing import List, Optional, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from ninja_extra import status
from ninja_extra.exceptions import APIException
from ninja_schema import ModelSchema, Schema, model_validator
from pydantic import validator

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