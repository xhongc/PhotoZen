from typing import List, Optional
from ninja_extra import ControllerBase, api_controller, route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from ninja import Form, Schema

from ninja.files import UploadedFile
from django.conf import settings
from django.http import FileResponse
from django.contrib.auth.models import User
from pydantic import BaseModel
import os
import mimetypes
from datetime import datetime
import shutil
from pathlib import Path
import PIL.Image
import io

from moment.schema import SuccessResponse
from applications.file.models import RecycleItem as DBRecycleItem

# 配置常量
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.md'],
    'video': ['.mp4', '.mov', '.avi'],
    'audio': ['.mp3', '.wav', '.ogg']
}

# 图片处理相关的常量
MAX_IMAGE_DIMENSION = 4096  # 最大图片尺寸
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
THUMBNAIL_SIZES = [(200, 200), (400, 400)]  # 缩略图尺寸列表

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

class UploadResponse(BaseModel):
    message: str
    path: str
    thumbnails: Optional[List[str]] = None

class UploadFileSchema(BaseModel):
    path: str

class DeleteFileSchema(BaseModel):
    path: str

class RecycleItemResponse(BaseModel):
    name: str
    path: str
    original_path: str
    size: Optional[int]
    delete_time: str
    remaining_days: int
    mime_type: Optional[str] = None
    preview_url: Optional[str] = None

class RecycleListResponse(BaseModel):
    items: List[RecycleItemResponse]
    total_count: int
    page: int
    page_size: int

class BatchOperationSchema(BaseModel):
    paths: List[str]

@api_controller("/files", auth=JWTAuth(), permissions=[IsAuthenticated])
class FileController(ControllerBase):
    model_config = {
        "arbitrary_types_allowed": True
    }

    def get_user_quota(self, user):
        """获取用户配额信息"""
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

    def validate_image(self, file: UploadedFile) -> tuple[bool, str]:
        """验证图片文件"""
        try:
            # 检查文件大小
            if file.size > MAX_UPLOAD_SIZE:
                return False, "图片大小超过限制"
                
                
            # 检查图片尺寸
            with PIL.Image.open(file) as img:
                if max(img.size) > MAX_IMAGE_DIMENSION:
                    return False, "图片尺寸过大"
                file.seek(0)
                
            return True, ""
        except Exception as e:
            return False, f"图片验证失败: {str(e)}"

    def process_image(self, file_path: str) -> list[str]:
        """处理上传的图片，生成不同尺寸的缩略图"""
        thumbnail_paths = []
        try:
            with PIL.Image.open(file_path) as img:
                # 转换为RGB模式（如果是RGBA）
                if img.mode in ('RGBA', 'LA'):
                    background = PIL.Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                # 生成不同尺寸的缩略图
                for width, height in THUMBNAIL_SIZES:
                    thumb = img.copy()
                    thumb.thumbnail((width, height), PIL.Image.Resampling.LANCZOS)
                    thumb_path = f"{file_path}_{width}x{height}.jpg"
                    thumb.save(thumb_path, "JPEG", quality=85)
                    thumbnail_paths.append(thumb_path)
                    
                # 优化原图
                img.save(file_path, "JPEG", quality=90, optimize=True)
                
        except Exception as e:
            print(f"图片处理失败: {str(e)}")
            
        return thumbnail_paths

    @route.post("/upload", response=UploadResponse)
    def upload_file(self, file: UploadedFile = None, data: Form[UploadFileSchema] = None):
        """上传文件到指定目录"""
            
        path = data.path
        try:
            # 检查用户配额
            quota = self.get_user_quota(self.context.request.user)
            if quota.used + file.size > quota.total:
                return UploadResponse(
                    message="存储空间不足",
                    path=""
                )

            # 构建用户特定的上传路径
            user_upload_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.username), path.strip("/"))
            os.makedirs(user_upload_path, exist_ok=True)
            
            file_path = os.path.join(user_upload_path, file.name)
            
            # 检查文件类型
            file_type = file.content_type
            
            if file_type.startswith('image/'):
                # 验证图片
                is_valid, error_msg = self.validate_image(file)
                if not is_valid:
                    return UploadResponse(
                        message=error_msg,
                        path=""
                    )
                    
                # 保存原始图片
                with open(file_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                        
                # 处理图片（生成缩略图等）
                thumbnail_paths = self.process_image(file_path)
                
                return UploadResponse(
                    message="图片上传成功",
                    path=file_path,
                    thumbnails=thumbnail_paths
                )
            else:
                # 处理非图片文件
                ext = os.path.splitext(file.name)[1].lower()
                if not any(ext in extensions for extensions in ALLOWED_EXTENSIONS.values()):
                    return UploadResponse(
                        message="不支持的文件类型",
                        path=""
                    )
                    
                with open(file_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                        
                return UploadResponse(
                    message="文件上传成功",
                    path=file_path
                )
                
        except Exception as e:
            return UploadResponse(
                message=str(e),
                path=""
            )

    @route.get("/preview/{path:path}")
    def preview_file(self, path: str):
        """获取文件预览"""
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.id), path)
            mime_type = magic.from_file(file_path)
            
            # 对于图片类型，返回缩略图
            if mime_type.startswith('image/'):
                thumb_path = f"{file_path}_thumb.jpg"
                if os.path.exists(thumb_path):
                    return FileResponse(open(thumb_path, 'rb'), content_type='image/jpeg')
            
            # 对于其他类型，返回原始文件
            return FileResponse(open(file_path, 'rb'), content_type=mime_type)
        except Exception as e:
            return {"error": str(e)}, 400

    @route.get("/download/{path:path}")
    def download_file(self, path: str):
        """下载文件"""
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.id), path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
                return response
            return {"error": "文件不存在"}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @route.post("/create-folder")
    def create_folder(self, path: str, name: str):
        """创建新文件夹"""
        try:
            new_folder_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.id), path.strip("/"), name)
            os.makedirs(new_folder_path, exist_ok=True)
            return {"message": "文件夹创建成功"}
        except Exception as e:
            return {"error": str(e)}, 400

    @route.get("/tree")
    def get_directory_tree(self, root: str = ""):
        """获取目录树结构"""
        base_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.id), root.strip("/"))
        
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

    @route.delete("/delete", response=SuccessResponse)
    def delete_item(self, data: DeleteFileSchema):
        """删除文件或文件夹(移入回收站)"""
        path = data.path
        try:
            # 获取用户回收站路径
            recycle_path = settings.RECYCLE_PATH
            # 确保回收站目录存在
            os.makedirs(recycle_path, exist_ok=True)
            
            # 源文件完整路径
            full_path = os.path.join(settings.MEDIA_ROOT, path.strip("/"))
            
            # 目标路径(回收站中)
            if path.startswith('/'):
                path = path[1:]
            dest_path = os.path.join(recycle_path, path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            # 如果目标路径已存在,添加时间戳
            if os.path.exists(dest_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{os.path.splitext(os.path.basename(path))[0]}_{timestamp}{os.path.splitext(path)[1]}"
                dest_path = os.path.join(recycle_path, filename)
            # 移动到回收站
            shutil.move(full_path, dest_path)
            size = os.path.getsize(dest_path)
            DBRecycleItem.objects.create(
                path=path,
                original_path=full_path,
                size=size,
                delete_time=datetime.now(),
                remaining_days=30
            )
            return {
                "msg": "已移入回收站",
                "result": True
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "msg": str(e),
                "result": False
            }

    @route.get("/quota", response=QuotaInfo)
    def get_quota(self):
        """获取用户存储配额信息"""
        return self.get_user_quota(self.context.request.user)

    @route.post("/move")
    def move_item(self, source: str, destination: str):
        """移动文件或文件夹"""
        try:
            user_base_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.id))
            source_path = os.path.join(user_base_path, source.strip("/"))
            dest_path = os.path.join(user_base_path, destination.strip("/"))
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            shutil.move(source_path, dest_path)
            return {"message": "移动成功"}
        except Exception as e:
            return {"error": str(e)}, 400

    @route.post("/copy")
    def copy_item(self, source: str, destination: str):
        """复制文件或文件夹"""
        try:
            user_base_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.id))
            source_path = os.path.join(user_base_path, source.strip("/"))
            dest_path = os.path.join(user_base_path, destination.strip("/"))
            
            # 检查配额
            quota = self.get_user_quota(self.context.request.user)
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

    @route.get("/recycle", response=RecycleListResponse)
    def get_recycle_list(self, page: int = 1, page_size: int = 20):
        """获取回收站列表"""
        try:
            # 从数据库获取回收站项目
            total_count = DBRecycleItem.objects.count()
            items = DBRecycleItem.objects.all()[(page-1)*page_size:page*page_size]

            # 转换为响应格式
            recycle_items = []
            for item in items:
                # 获取文件类型
                mime_type = mimetypes.guess_type(item.path)[0]
                
                recycle_item = RecycleItemResponse(
                    name=os.path.basename(item.path),
                    path=item.path,
                    original_path=item.original_path,
                    size=item.size,
                    delete_time=item.delete_time.strftime('%Y-%m-%d %H:%M:%S'),
                    remaining_days=item.remaining_days,
                    mime_type=mime_type,
                    preview_url=f"/api/files/preview/{item.path}" if mime_type and mime_type.startswith('image/') else None
                )
                recycle_items.append(recycle_item)

            return RecycleListResponse(
                items=recycle_items,
                total_count=total_count,
                page=page,
                page_size=page_size
            )
        except Exception as e:
            return RecycleListResponse(
                items=[],
                total_count=0,
                page=page,
                page_size=page_size
            )

    @route.post("/recycle/restore", response=SuccessResponse)
    def restore_file(self, path: str):
        """恢复文件"""
        try:
            # 从数据库获取回收项
            recycle_item = DBRecycleItem.objects.get(path=path)
            recycle_path = settings.RECYCLE_PATH
            file_path = os.path.join(recycle_path, path)
            
            if not os.path.exists(file_path):
                return {
                    "msg": "文件不存在",
                    "result": False
                }
            
            # 获取原始路径
            original_path = os.path.join(settings.MEDIA_ROOT, str(self.context.request.user.id), recycle_item.original_path)
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            
            # 移动文件
            shutil.move(file_path, original_path)
            
            # 从数据库删除记录
            recycle_item.delete()
            
            return {
                "msg": "文件已恢复",
                "result": True
            }
        except DBRecycleItem.DoesNotExist:
            return {
                "msg": "回收项不存在",
                "result": False
            }
        except Exception as e:
            return {
                "msg": str(e),
                "result": False
            }

    @route.post("/recycle/restore-batch", response=SuccessResponse)
    def restore_files_batch(self, data: BatchOperationSchema):
        """批量恢复文件"""
        try:
            success_count = 0
            for path in data.paths:
                result = self.restore_file(path)
                if result["result"]:
                    success_count += 1
            
            return {
                "msg": f"成功恢复 {success_count}/{len(data.paths)} 个文件",
                "result": True
            }
        except Exception as e:
            return {
                "msg": str(e),
                "result": False
            }

    @route.delete("/recycle/delete", response=SuccessResponse)
    def delete_from_recycle(self, path: str):
        """从回收站永久删除文件"""
        try:
            recycle_path = settings.RECYCLE_PATH
            file_path = os.path.join(recycle_path, path)
            
            if not os.path.exists(file_path):
                return {
                    "msg": "文件不存在",
                    "result": False
                }
            
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            
            return {
                "msg": "文件已永久删除",
                "result": True
            }
        except Exception as e:
            return {
                "msg": str(e),
                "result": False
            }

    @route.delete("/recycle/delete-batch", response=SuccessResponse)
    def delete_from_recycle_batch(self, data: BatchOperationSchema):
        """批量从回收站永久删除文件"""
        try:
            success_count = 0
            for path in data.paths:
                result = self.delete_from_recycle(path)
                if result["result"]:
                    success_count += 1
            
            return {
                "msg": f"成功删除 {success_count}/{len(data.paths)} 个文件",
                "result": True
            }
        except Exception as e:
            return {
                "msg": str(e),
                "result": False
            }
