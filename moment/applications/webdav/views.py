from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from components.djangodav.views.views import DavView
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import base64
from ninja_jwt.authentication import JWTAuth

@method_decorator(csrf_exempt, name='dispatch')
class AuthenticatedDavView(DavView):
    """添加认证功能的 WebDAV 视图"""
    
    def dispatch(self, request, path, *args, **kwargs):
        # 获取认证信息
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header:
            response = HttpResponse(status=401)
            response['WWW-Authenticate'] = 'Basic realm="WebDAV"'
            response['DAV'] = '1, 2'
            return response
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user = JWTAuth().jwt_authenticate(request, token)
            request.user = user
        elif auth_header.startswith('Basic '):
            # 解析认证信息
            try:
                auth_decoded = base64.b64decode(auth_header.split(' ')[1]).decode('utf-8')
                username, password = auth_decoded.split(':')
            except:
                response = HttpResponse(status=401)
                response['WWW-Authenticate'] = 'Basic realm="WebDAV"'
                response['DAV'] = '1, 2'
                return response
                
            # 验证用户
            user = authenticate(username=username, password=password)
            if user is None:
                response = HttpResponse(status=401)
                response['WWW-Authenticate'] = 'Basic realm="WebDAV"'
                response['DAV'] = '1, 2'
                return response
                
            # 将用户信息添加到请求中
            request.user = user
        else:
            response = HttpResponse(status=401)
            response['WWW-Authenticate'] = 'Basic realm="WebDAV"'
            response['DAV'] = '1, 2'
            return response
                
        # 调用父类的 dispatch 方法
        response = super().dispatch(request, path, *args, **kwargs)    
        return response
        
    def get_access(self, resource):
        """根据用户权限返回访问控制"""
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return self.acl_class(read=False, write=False, delete=False, full=False)
            
        # 这里可以根据用户权限返回不同的访问控制
        # 例如：管理员有所有权限，普通用户只有读写权限等
        if self.request.user.is_superuser:
            return self.acl_class(read=True, write=True, delete=True, full=True)
        else:
            return self.acl_class(read=True, write=True, delete=False, full=False)
            
    def no_access(self):
        """重写 no_access 方法，确保返回正确的认证头"""
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="WebDAV"'
        response['DAV'] = '1, 2'
        return response

# Create your views here.
