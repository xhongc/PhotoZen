from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from typing import Dict, Any, Optional, Tuple
import json
import os
from django.core.exceptions import ValidationError
from .models import Photo


class PhotoMetadataEditor:
    """
    照片元数据编辑器类
    支持查看、编辑EXIF数据和自定义字段
    """
    
    # 常用EXIF标签映射到中文名称
    EXIF_TAGS_CHINESE = {
        'DateTime': '拍摄时间',
        'DateTimeOriginal': '原始拍摄时间', 
        'DateTimeDigitized': '数字化时间',
        'Make': '相机制造商',
        'Model': '相机型号',
        'Software': '软件',
        'Artist': '作者',
        'Copyright': '版权信息',
        'ImageWidth': '图像宽度',
        'ImageLength': '图像高度',
        'XResolution': '水平分辨率',
        'YResolution': '垂直分辨率',
        'ResolutionUnit': '分辨率单位',
        'ExifImageWidth': 'EXIF图像宽度',
        'ExifImageHeight': 'EXIF图像高度',
        'FNumber': '光圈值',
        'ExposureTime': '曝光时间',
        'ISOSpeedRatings': 'ISO感光度',
        'FocalLength': '焦距',
        'Flash': '闪光灯',
        'WhiteBalance': '白平衡',
        'ExposureMode': '曝光模式',
        'MeteringMode': '测光模式',
        'SceneCaptureType': '场景类型',
        'ColorSpace': '色彩空间',
        'Orientation': '旋转信息',
        'GPSLatitude': 'GPS纬度',
        'GPSLongitude': 'GPS经度',
        'GPSAltitude': 'GPS海拔',
        'GPSTimeStamp': 'GPS时间戳',
    }
    
    # 可编辑的EXIF字段
    EDITABLE_EXIF_TAGS = {
        'DateTime', 'DateTimeOriginal', 'DateTimeDigitized',
        'Artist', 'Copyright', 'Software', 'ImageDescription'
    }
    
    def __init__(self, photo: Photo):
        """
        初始化元数据编辑器
        
        Args:
            photo: Photo模型实例
        """
        self.photo = photo
        self._exif_data = None
        self._image = None
    
    def _get_image(self) -> Image.Image:
        """获取PIL Image对象"""
        if self._image is None:
            image_path = self.photo.file_path.path
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"图片文件不存在: {image_path}")
            self._image = Image.open(image_path)
        return self._image
    
    def _get_exif_data(self) -> Dict[str, Any]:
        """获取EXIF数据"""
        if self._exif_data is None:
            image = self._get_image()
            exif_dict = {}
            
            if hasattr(image, '_getexif') and image._getexif() is not None:
                exif_data = image._getexif()
                
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    # 处理GPS数据
                    if tag == 'GPSInfo':
                        gps_dict = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_dict[gps_tag] = gps_value
                        exif_dict[tag] = gps_dict
                    else:
                        # 转换特殊类型的值
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8', errors='ignore')
                            except:
                                value = str(value)
                        elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):
                            # 处理Ratio类型
                            if value.denominator != 0:
                                value = float(value.numerator) / float(value.denominator)
                            else:
                                value = float(value.numerator)
                        
                        exif_dict[tag] = value
            
            self._exif_data = exif_dict
        
        return self._exif_data
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        获取所有元数据（包括EXIF和自定义字段）
        
        Returns:
            包含所有元数据的字典
        """
        metadata = {
            'basic_info': {
                'id': self.photo.id,
                'title': self.photo.title,
                'description': self.photo.description,
                'file_path': str(self.photo.file_path),
                'upload_time': self.photo.upload_time.isoformat(),
                'taken_time': self.photo.taken_time.isoformat(),
                'size': self.photo.size,
                'width': self.photo.width,
                'height': self.photo.height,
                'format': self.photo.format,
            },
            'exif_data': {},
            'custom_fields': {}
        }
        
        # 获取EXIF数据
        exif_data = self._get_exif_data()
        for tag, value in exif_data.items():
            chinese_name = self.EXIF_TAGS_CHINESE.get(tag, tag)
            metadata['exif_data'][tag] = {
                'name': chinese_name,
                'value': value,
                'editable': tag in self.EDITABLE_EXIF_TAGS
            }
        
        # 获取自定义字段
        custom_metadata = self.photo.custom_metadata.all()
        for field in custom_metadata:
            metadata['custom_fields'][field.key] = {
                'name': field.name,
                'value': field.value,
                'field_type': field.field_type,
                'editable': True
            }
        
        return metadata
    
    def get_exif_data(self) -> Dict[str, Any]:
        """
        仅获取EXIF数据
        
        Returns:
            EXIF数据字典
        """
        return self._get_exif_data()
    
    def update_exif_field(self, tag: str, value: Any) -> bool:
        """
        更新单个EXIF字段
        
        Args:
            tag: EXIF标签名
            value: 新值
            
        Returns:
            是否更新成功
        """
        if tag not in self.EDITABLE_EXIF_TAGS:
            raise ValidationError(f"EXIF字段 '{tag}' 不可编辑")
        
        try:
            image = self._get_image()
            exif_dict = image._getexif() or {}
            
            # 查找标签ID
            tag_id = None
            for tid, tname in TAGS.items():
                if tname == tag:
                    tag_id = tid
                    break
            
            if tag_id is None:
                raise ValidationError(f"未知的EXIF标签: {tag}")
            
            # 更新EXIF数据
            exif_dict[tag_id] = value
            
            # 保存更改后的图片（注意：这会修改原文件）
            # 在实际应用中可能需要备份原文件
            image.save(self.photo.file_path.path, exif=exif_dict)
            
            # 清除缓存，强制重新加载
            self._exif_data = None
            self._image = None
            
            return True
            
        except Exception as e:
            raise ValidationError(f"更新EXIF字段失败: {str(e)}")
    
    def add_custom_field(self, key: str, name: str, value: Any, 
                        field_type: str = 'text') -> 'PhotoMetadata':
        """
        添加自定义字段
        
        Args:
            key: 字段键名
            name: 字段显示名称
            value: 字段值
            field_type: 字段类型 (text, number, date, boolean)
            
        Returns:
            创建的PhotoMetadata实例
        """
        from .models import PhotoMetadata
        
        # 验证字段类型
        if field_type not in ['text', 'number', 'date', 'boolean', 'json']:
            raise ValidationError("无效的字段类型")
        
        # 验证和转换值
        if field_type == 'json' and not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        
        metadata, created = PhotoMetadata.objects.update_or_create(
            photo=self.photo,
            key=key,
            defaults={
                'name': name,
                'value': str(value),
                'field_type': field_type
            }
        )
        
        return metadata
    
    def update_custom_field(self, key: str, value: Any) -> bool:
        """
        更新自定义字段值
        
        Args:
            key: 字段键名
            value: 新值
            
        Returns:
            是否更新成功
        """
        try:
            metadata = self.photo.custom_metadata.get(key=key)
            
            # 根据字段类型验证和转换值
            if metadata.field_type == 'json' and not isinstance(value, str):
                value = json.dumps(value, ensure_ascii=False)
            
            metadata.value = str(value)
            metadata.save()
            return True
            
        except Exception as e:
            raise ValidationError(f"更新自定义字段失败: {str(e)}")
    
    def remove_custom_field(self, key: str) -> bool:
        """
        删除自定义字段
        
        Args:
            key: 字段键名
            
        Returns:
            是否删除成功
        """
        try:
            metadata = self.photo.custom_metadata.get(key=key)
            metadata.delete()
            return True
        except Exception:
            return False
    
    def get_gps_coordinates(self) -> Optional[Tuple[float, float]]:
        """
        获取GPS坐标
        
        Returns:
            (纬度, 经度) 元组，如果没有GPS信息则返回None
        """
        exif_data = self._get_exif_data()
        gps_info = exif_data.get('GPSInfo', {})
        
        if not gps_info:
            return None
        
        try:
            # 获取GPS坐标
            lat_ref = gps_info.get('GPSLatitudeRef', 'N')
            lat = gps_info.get('GPSLatitude', [])
            lon_ref = gps_info.get('GPSLongitudeRef', 'E')
            lon = gps_info.get('GPSLongitude', [])
            
            if not lat or not lon:
                return None
            
            # 转换为十进制度数
            def dms_to_decimal(dms, ref):
                degrees = float(dms[0])
                minutes = float(dms[1]) if len(dms) > 1 else 0
                seconds = float(dms[2]) if len(dms) > 2 else 0
                
                decimal = degrees + minutes/60 + seconds/3600
                if ref in ['S', 'W']:
                    decimal = -decimal
                
                return decimal
            
            latitude = dms_to_decimal(lat, lat_ref)
            longitude = dms_to_decimal(lon, lon_ref)
            
            return (latitude, longitude)
            
        except (IndexError, ValueError, TypeError):
            return None
    
    def get_camera_info(self) -> Dict[str, str]:
        """
        获取相机信息
        
        Returns:
            包含相机制造商、型号等信息的字典
        """
        exif_data = self._get_exif_data()
        
        return {
            'make': exif_data.get('Make', '未知'),
            'model': exif_data.get('Model', '未知'),
            'software': exif_data.get('Software', '未知'),
            'lens_model': exif_data.get('LensModel', '未知'),
        }
    
    def get_shooting_parameters(self) -> Dict[str, Any]:
        """
        获取拍摄参数
        
        Returns:
            包含光圈、快门、ISO等拍摄参数的字典
        """
        exif_data = self._get_exif_data()
        
        return {
            'aperture': exif_data.get('FNumber', '未知'),
            'shutter_speed': exif_data.get('ExposureTime', '未知'),
            'iso': exif_data.get('ISOSpeedRatings', '未知'),
            'focal_length': exif_data.get('FocalLength', '未知'),
            'flash': exif_data.get('Flash', '未知'),
            'white_balance': exif_data.get('WhiteBalance', '未知'),
            'exposure_mode': exif_data.get('ExposureMode', '未知'),
            'metering_mode': exif_data.get('MeteringMode', '未知'),
        }