import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection, transaction
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .log.log import Logger

logger = Logger()


class GetFansList(APIView):
    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request_path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            # 用户未登录
            if not request.user.is_authenticated:
                return JsonResponse({'status': 401, 'msg': '用户未登录'}, status=401)
            user_id = request.user.id
            data = json.loads(request.body.decode('utf-8'))
            get_follow_sql = '''
            select follow_table.id,follow_table.target_user_id,follow_table.operation_user_id,
            follow_table.operation_time,follow_table.follow_status,auth_user.id as user_id,
            auth_user.username,auth_user.avatar_path
             from follow_table
            left join auth_user on auth_user.id=follow_table.operation_user_id
             where target_user_id=%s limit %s offset %s
            '''
            with connection.cursor() as cursor:
                cursor.execute(get_follow_sql, (user_id, data.get('limit', 10), data.get('offset', 0)))
                result = cursor.fetchall()
                rows = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
                return JsonResponse({'status': 200, 'data': rows}, status=200)

        except Exception as e:
            logger.error(e)
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
