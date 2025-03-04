from django.contrib.auth import get_user_model
from ninja_extra import api_controller, route
from ninja_extra.pagination import (
    PageNumberPaginationExtra,
    PaginatedResponseSchema,
    paginate,
)
from ninja_extra.permissions import IsAuthenticated
from ninja_extra.shortcuts import get_object_or_exception
from ninja_jwt.authentication import JWTAuth
from ninja_extra import ControllerBase
from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile
from django.shortcuts import get_object_or_404
from typing import List

from applications.photos.schema import PhotoSchema
from .models import Photo, Album, Tag
from PIL import Image
import os
from datetime import datetime
from ninja_jwt.authentication import JWTAuth
from ninja_extra import ControllerBase
User = get_user_model()




@api_controller("/photos", auth=JWTAuth(), permissions=[IsAuthenticated])
class PhotoController(ControllerBase):
    @route.get(
        "photos/",
        response=PaginatedResponseSchema[PhotoSchema],
        url_name="photos",
    )
    @paginate(PageNumberPaginationExtra)
    def list(self):
        return Photo.objects.all()

    