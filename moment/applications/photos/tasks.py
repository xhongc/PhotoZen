import os
from PIL import Image
from django.conf import settings
from django.utils import timezone
from .models import Photo
from datetime import datetime

def scan_media_directory():
    """
    扫描 media 目录下的图片文件并创建 Photo 记录
    支持的图片格式：JPG, JPEG, PNG, GIF
    """
    media_root = settings.PHOTO_FOLDER_PREFIX
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif'}
    
    # 用于批量创建的照片列表
    photos_to_create = []
    
    # 遍历 media 目录
    for root, dirs, files in os.walk(media_root):
        for file in files:
            # 检查文件扩展名
            ext = os.path.splitext(file)[1].lower()
            if ext not in supported_formats:
                continue
                
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, media_root)
            
            # 检查是否已经存在该照片记录
            if Photo.objects.filter(file_path=relative_path).exists():
                continue
                
            try:
                # 获取图片信息
                with Image.open(file_path) as img:
                    width, height = img.size
                    format = img.format.upper()
                    
                # 获取文件大小
                size = os.path.getsize(file_path)
                
                # 获取文件修改时间作为拍摄时间
                taken_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # 添加到批量创建列表
                photos_to_create.append(
                    Photo(
                        title=os.path.splitext(file)[0],
                        description=f"从媒体目录导入的照片",
                        file_path=relative_path,
                        taken_time=taken_time,
                        size=size,
                        width=width,
                        height=height,
                        format=format
                    )
                )
                
                print(f"准备导入照片: {file}")
                
                # 每500张照片批量创建一次
                if len(photos_to_create) >= 500:
                    Photo.objects.bulk_create(photos_to_create)
                    print(f"已批量导入 {len(photos_to_create)} 张照片")
                    photos_to_create = []  # 清空列表，准备下一批
                
            except Exception as e:
                print(f"处理照片 {file} 时出错: {str(e)}")
                continue
    
    # 处理剩余的照片记录
    if photos_to_create:
        Photo.objects.bulk_create(photos_to_create)
        print(f"已批量导入剩余的 {len(photos_to_create)} 张照片")
