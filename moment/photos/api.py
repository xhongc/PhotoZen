from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile
from django.shortcuts import get_object_or_404
from typing import List
from .models import Photo, Album, Tag
from PIL import Image
import os
from datetime import datetime

api = NinjaAPI()

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

# Photo endpoints
@api.post("/photos/upload")
def upload_photo(request, file: UploadedFile = File(...), title: str = None, description: str = None):
    # Open image to get metadata
    img = Image.open(file)
    width, height = img.size
    
    # Create photo object
    photo = Photo.objects.create(
        title=title or file.name,
        description=description or "",
        file_path=file,
        size=file.size,
        width=width,
        height=height,
        format=img.format
    )
    
    # Create thumbnail
    thumbnail_size = (300, 300)
    img.thumbnail(thumbnail_size)
    thumbnail_path = f"thumbnails/{file.name}"
    img.save(thumbnail_path)
    photo.thumbnail_path = thumbnail_path
    photo.save()

    return {"id": photo.id}

@api.get("/photos", response=List[PhotoSchema])
def list_photos(request):
    return [
        PhotoSchema(
            id=1,
            title="test1",
            description="test1",
            file_path="/media/photos/2023/02/27/1.jpg",
            thumbnail_path="/media/thumbnails/2023/02/27/1.jpg",
            upload_time=datetime(2023, 2, 27),
            taken_time=datetime(2023, 2, 27),
            size=1024,
            width=1024,
            height=768,
            format="JPEG",
            albums=[
                AlbumSchema(id=1, name="test1", description="test1", created_time=datetime(2023, 2, 27), updated_time=datetime(2023, 2, 27)),
                AlbumSchema(id=2, name="test2", description="test2", created_time=datetime(2023, 2, 27), updated_time=datetime(2023, 2, 27)),
            ],
            tags=[
                TagSchema(id=1, name="test1"),
                TagSchema(id=2, name="test2"),
            ],
        ),
        PhotoSchema(
            id=2,
            title="test2",
            description="test2",
            file_path="/media/photos/2023/02/27/2.jpg",
            thumbnail_path="/media/thumbnails/2023/02/27/2.jpg",
            upload_time=datetime(2023, 2, 27),
            taken_time=datetime(2023, 2, 27),
            size=1024,
            width=1024,
            height=768,
            format="JPEG",
           albums=[
                AlbumSchema(id=1, name="test1", description="test1", created_time=datetime(2023, 2, 27), updated_time=datetime(2023, 2, 27)),
                AlbumSchema(id=2, name="test2", description="test2", created_time=datetime(2023, 2, 27), updated_time=datetime(2023, 2, 27)),
            ],
            tags=[
                TagSchema(id=1, name="test1"),
                TagSchema(id=2, name="test2"),
            ],
        ),
    ]

@api.get("/photos/{photo_id}", response=PhotoSchema)
def get_photo(request, photo_id: int):
    return get_object_or_404(Photo, id=photo_id)

# Album endpoints
@api.post("/albums")
def create_album(request, name: str, description: str = ""):
    album = Album.objects.create(name=name, description=description)
    return {"id": album.id}

@api.get("/albums", response=List[AlbumSchema])
def list_albums(request):
    return Album.objects.all()

# Tag endpoints
@api.post("/tags")
def create_tag(request, name: str):
    tag, created = Tag.objects.get_or_create(name=name)
    return {"id": tag.id}

@api.get("/tags", response=List[TagSchema])
def list_tags(request):
    return Tag.objects.all()

# Photo management endpoints
@api.post("/photos/{photo_id}/albums/{album_id}")
def add_to_album(request, photo_id: int, album_id: int):
    photo = get_object_or_404(Photo, id=photo_id)
    album = get_object_or_404(Album, id=album_id)
    photo.albums.add(album)
    return {"success": True}

@api.post("/photos/{photo_id}/tags/{tag_name}")
def add_tag(request, photo_id: int, tag_name: str):
    photo = get_object_or_404(Photo, id=photo_id)
    tag, _ = Tag.objects.get_or_create(name=tag_name)
    photo.tags.add(tag)
    return {"success": True}
