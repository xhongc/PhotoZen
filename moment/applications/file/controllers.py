from typing import List, Optional
from ninja import Router, File, Form
from ninja.files import UploadedFile
from ninja.security import HttpBearer
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from pydantic import BaseModel
import os
import mimetypes
from datetime import datetime
import shutil
from pathlib import Path
import magic
import PIL.Image

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # 这里替换为你的实际token验证逻辑
            user = User.objects.get(auth_token__key=token)
            return user
        except User.DoesNotExist:
            return None

router = Router(auth=AuthBearer())

# 配置常量
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.md'],
    'video': ['.mp4', '.mov', '.avi'],
    'audio': ['.mp3', '.wav', '.ogg']
}

class FileItem(BaseModel):
    name: str
    path: str
    type: str
    size: Optional[int]
    modified_date: str
    is_dir: bool
    preview_url: Optional[str] = None
    mime_type: Optional[str] = None

class DirectoryResponse(BaseModel):
    items: List[FileItem]
    total_count: int
    folder_count: int
    file_count: int
    total_size: int
    quota_used: float  # 百分比

class QuotaInfo(BaseModel):
    used: int
    total: int
    percentage: float

def get_mime_type(file_path):
    """获取文件的MIME类型"""
    mime = magic.Magic(mime=True)
    return mime.from_file(file_path)

def is_file_allowed(filename, mime_type):
    """检查文件类型是否允许"""
    ext = os.path.splitext(filename)[1].lower()
    for extensions in ALLOWED_EXTENSIONS.values():
        if ext in extensions:
            return True
    return False

def get_user_quota(user):
    """获取用户配额信息"""
    # 这里替换为实际的用户配额逻辑
    total_quota = 1024 * 1024 * 1024  # 1GB
    used_quota = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for dirpath, _, filenames in os.walk(os.path.join(settings.MEDIA_ROOT, str(user.id)))
        for filename in filenames
    )
    return QuotaInfo(
        used=used_quota,
        total=total_quota,
        percentage=(used_quota / total_quota) * 100
    )

def create_thumbnail(image_path, size=(200, 200)):
    """为图片创建缩略图"""
    try:
        with PIL.Image.open(image_path) as img:
            img.thumbnail(size)
            thumbnail_path = f"{image_path}_thumb.jpg"
            img.save(thumbnail_path, "JPEG")
            return thumbnail_path
    except Exception:
        return None

@router.get("/list")
def list_directory(request, path: str = ""):
    """获取指定目录下的文件和文件夹列表"""
    user_base_path = os.path.join(settings.MEDIA_ROOT, str(request.auth.id))
    base_path = os.path.join(user_base_path, path.strip("/"))
    items = []
    folder_count = 0
    file_count = 0
    total_size = 0

    try:
        for entry in os.scandir(base_path):
            modified_time = datetime.fromtimestamp(entry.stat().st_mtime)
            mime_type = None
            preview_url = None
            
            if entry.is_dir():
                folder_count += 1
                size = None
                file_type = "文件夹"
            else:
                file_count += 1
                size = entry.stat().st_size
                total_size += size
                ext = os.path.splitext(entry.name)[1].lower()
                file_type = ext[1:].upper() + " 文件" if ext else "文件"
                mime_type = get_mime_type(entry.path)
                
                # 为图片生成预览URL
                if mime_type.startswith('image/'):
                    preview_url = f"/api/file/preview/{os.path.relpath(entry.path, settings.MEDIA_ROOT)}"

            items.append(FileItem(
                name=entry.name,
                path=os.path.join(path, entry.name),
                type=file_type,
                size=size,
                modified_date=modified_time.strftime("%Y/%m/%d"),
                is_dir=entry.is_dir(),
                preview_url=preview_url,
                mime_type=mime_type
            ))

        quota = get_user_quota(request.auth)
        
        return DirectoryResponse(
            items=sorted(items, key=lambda x: (not x.is_dir, x.name)),
            total_count=len(items),
            folder_count=folder_count,
            file_count=file_count,
            total_size=total_size,
            quota_used=quota.percentage
        )
    except Exception as e:
        return {"error": str(e)}, 400

@router.post("/upload")
def upload_file(request, file: UploadedFile = File(...), path: str = Form(...)):
    """上传文件到指定目录"""
    try:
        # 检查文件大小
        if file.size > MAX_UPLOAD_SIZE:
            return {"error": "文件大小超过限制"}, 400

        # 检查用户配额
        quota = get_user_quota(request.auth)
        if quota.used + file.size > quota.total:
            return {"error": "存储空间不足"}, 400

        # 检查文件类型
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)  # 重置文件指针
        if not is_file_allowed(file.name, mime_type):
            return {"error": "不支持的文件类型"}, 400

        # 构建用户特定的上传路径
        user_upload_path = os.path.join(settings.MEDIA_ROOT, str(request.auth.id), path.strip("/"))
        os.makedirs(user_upload_path, exist_ok=True)
        
        file_path = os.path.join(user_upload_path, file.name)
        
        # 保存文件
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # 如果是图片，创建缩略图
        if mime_type.startswith('image/'):
            create_thumbnail(file_path)
                
        return {"message": "文件上传成功"}
    except Exception as e:
        return {"error": str(e)}, 400

@router.get("/preview/{path:path}")
def preview_file(request, path: str):
    """获取文件预览"""
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, str(request.auth.id), path)
        mime_type = get_mime_type(file_path)
        
        # 对于图片类型，返回缩略图
        if mime_type.startswith('image/'):
            thumb_path = f"{file_path}_thumb.jpg"
            if os.path.exists(thumb_path):
                return FileResponse(open(thumb_path, 'rb'), content_type='image/jpeg')
        
        # 对于其他类型，返回原始文件
        return FileResponse(open(file_path, 'rb'), content_type=mime_type)
    except Exception as e:
        return {"error": str(e)}, 400

@router.get("/download/{path:path}")
def download_file(request, path: str):
    """下载文件"""
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, str(request.auth.id), path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
            return response
        return {"error": "文件不存在"}, 404
    except Exception as e:
        return {"error": str(e)}, 400

@router.post("/create-folder")
def create_folder(request, path: str, name: str):
    """创建新文件夹"""
    try:
        new_folder_path = os.path.join(settings.MEDIA_ROOT, path.strip("/"), name)
        os.makedirs(new_folder_path, exist_ok=True)
        return {"message": "文件夹创建成功"}
    except Exception as e:
        return {"error": str(e)}, 400

@router.get("/tree")
def get_directory_tree(request, root: str = ""):
    """获取目录树结构"""
    base_path = os.path.join(settings.MEDIA_ROOT, root.strip("/"))
    
    def scan_directory(path):
        items = []
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    items.append({
                        "name": entry.name,
                        "path": os.path.relpath(entry.path, settings.MEDIA_ROOT),
                        "children": scan_directory(entry.path) if entry.is_dir() else None
                    })
        except Exception:
            pass
        return items

    return {"tree": scan_directory(base_path)}

@router.delete("/delete")
def delete_item(request, path: str):
    """删除文件或文件夹"""
    try:
        full_path = os.path.join(settings.MEDIA_ROOT, path.strip("/"))
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)
        return {"message": "删除成功"}
    except Exception as e:
        return {"error": str(e)}, 400

@router.get("/quota")
def get_quota(request):
    """获取用户存储配额信息"""
    return get_user_quota(request.auth)

@router.post("/move")
def move_item(request, source: str, destination: str):
    """移动文件或文件夹"""
    try:
        user_base_path = os.path.join(settings.MEDIA_ROOT, str(request.auth.id))
        source_path = os.path.join(user_base_path, source.strip("/"))
        dest_path = os.path.join(user_base_path, destination.strip("/"))
        
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        shutil.move(source_path, dest_path)
        return {"message": "移动成功"}
    except Exception as e:
        return {"error": str(e)}, 400

@router.post("/copy")
def copy_item(request, source: str, destination: str):
    """复制文件或文件夹"""
    try:
        user_base_path = os.path.join(settings.MEDIA_ROOT, str(request.auth.id))
        source_path = os.path.join(user_base_path, source.strip("/"))
        dest_path = os.path.join(user_base_path, destination.strip("/"))
        
        # 检查配额
        quota = get_user_quota(request.auth)
        if os.path.isfile(source_path):
            required_space = os.path.getsize(source_path)
        else:
            required_space = sum(os.path.getsize(os.path.join(dirpath, f))
                               for dirpath, _, filenames in os.walk(source_path)
                               for f in filenames)
        
        if quota.used + required_space > quota.total:
            return {"error": "存储空间不足"}, 400
            
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        if os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path)
        else:
            shutil.copy2(source_path, dest_path)
            
        return {"message": "复制成功"}
    except Exception as e:
        return {"error": str(e)}, 400
