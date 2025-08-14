from ninja import Schema
from typing import Dict, Any, Optional, List
from datetime import datetime


class MetadataFieldSchema(Schema):
    """元数据字段Schema"""
    name: str
    value: Any
    editable: bool
    field_type: Optional[str] = None


class PhotoMetadataSchema(Schema):
    """照片完整元数据Schema"""
    basic_info: Dict[str, Any]
    exif_data: Dict[str, MetadataFieldSchema]
    custom_fields: Dict[str, MetadataFieldSchema]


class ExifDataSchema(Schema):
    """EXIF数据Schema"""
    data: Dict[str, Any]


class CustomFieldCreateSchema(Schema):
    """创建自定义字段Schema"""
    key: str
    name: str
    value: str
    field_type: str = 'text'


class CustomFieldUpdateSchema(Schema):
    """更新自定义字段Schema"""
    value: str


class ExifFieldUpdateSchema(Schema):
    """更新EXIF字段Schema"""
    tag: str
    value: str


class GPSCoordinatesSchema(Schema):
    """GPS坐标Schema"""
    latitude: float
    longitude: float


class CameraInfoSchema(Schema):
    """相机信息Schema"""
    make: str
    model: str
    software: str
    lens_model: str


class ShootingParametersSchema(Schema):
    """拍摄参数Schema"""
    aperture: Any
    shutter_speed: Any
    iso: Any
    focal_length: Any
    flash: Any
    white_balance: Any
    exposure_mode: Any
    metering_mode: Any


class PhotoMetadataDetailSchema(Schema):
    """照片元数据详细信息Schema"""
    id: int
    key: str
    name: str
    value: str
    field_type: str
    created_time: datetime
    updated_time: datetime


class MetadataResponseSchema(Schema):
    """元数据操作响应Schema"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None