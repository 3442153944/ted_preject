from datetime import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
import json
from ..log.log import Logger
from django.http import JsonResponse

logger = Logger()

class AdminCheck(APIView):
    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            is_auth = request.user.is_authenticated
            if is_auth is None or is_auth is False:
                return JsonResponse({'status':403,'msg':'未登录'},status=403)
            admin_id = request.user.id
            if admin_id is None or admin_id == 0:
                return JsonResponse({'status':403,'msg':'未登录'},status=403)

            with connection.cursor() as cursor:
                permission_check_sql='''
                select is_superuser from auth_user where id=%s
                '''
                cursor.execute(permission_check_sql, [admin_id])
                result = cursor.fetchone()
                if result[0] is None or result[0] is False:
                    return JsonResponse({'status':403,'msg':'权限不足'},status=403)
                elif result[0] is True or result[0] == 1 or result[0] == '1':
                    return JsonResponse({'status':200,'msg':'权限正常'},status=200)
                return JsonResponse({'status':403,'msg':'权限不足'},status=403)

        except Exception as e:
            logger.error(self.request_path(request) + str(e))
            return JsonResponse({'status':500,'msg':'服务器内部错误'},status=500)