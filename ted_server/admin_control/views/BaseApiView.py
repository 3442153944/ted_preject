# views/base_view.py

from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import DatabaseError
from datetime import datetime
from ..log.log import Logger

logger = Logger()


class BaseAPIView(APIView):
    def request_path(self, request):
        """获取请求的详细路径信息，用于日志记录"""
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def log_warning(self, request, message="页面不存在"):
        """通用警告日志记录"""
        logger.warning(f"{self.request_path(request)} {message}")

    def log_error(self, request, error):
        """通用错误日志记录"""
        logger.error(f"{self.request_path(request)}, 服务器错误：{error}")

    def handle_database_error(self, request, db_error):
        """通用数据库错误处理"""
        self.log_error(request, db_error)
        return JsonResponse({'status': 500, 'msg': '数据库错误，操作失败'}, status=500)

    def get(self, request, *args, **kwargs):
        """通用 GET 方法，返回 404 错误"""
        self.log_warning(request, "尝试访问不支持的资源")
        return JsonResponse({'status': 404, 'msg': '页面不存在'}, status=404)

    def check_admin_permission(self, request):
        """通用管理员权限验证"""
        if not request.user.is_authenticated:
            return JsonResponse({'status': 403, 'msg': '未登录'}, status=403)

        if not request.user.is_superuser:
            return JsonResponse({'status': 403, 'msg': '权限不足，管理员认证失败'}, status=403)

        return None  # 权限验证通过
