from applications.photos.schema import PhotoSchema
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

from .models import Photo

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
