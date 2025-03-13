from datetime import datetime
from typing import List, Optional
from ninja import Schema
from pydantic import Field

class TagSchema(Schema):
    id: int
    name: str

class LocationSchema(Schema):
    latitude: float
    longitude: float
    name: str

class PhotoUploadSchema(Schema):
    title: str
    description: Optional[str] = None
    taken_time: Optional[datetime] = None
    location: Optional[LocationSchema] = None
    tags: Optional[List[str]] = None
    albums: Optional[List[int]] = None

class PhotoUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    taken_time: Optional[datetime] = None
    location: Optional[LocationSchema] = None
    tags: Optional[List[str]] = None
    albums: Optional[List[int]] = None

class PhotoRatingSchema(Schema):
    rating: float = Field(ge=0, le=5)  # 评分范围0-5
    comment: Optional[str] = None

class PhotoSchema(Schema):
    id: int
    title: str
    description: str
    file_path: str
    thumbnail_path: str
    upload_time: datetime
    taken_time: Optional[datetime] = None
    size: int
    width: int
    height: int
    format: str
    location: Optional[LocationSchema] = None
    rating: Optional[float] = None
    is_favorite: bool = False
    tags: List[TagSchema]