from datetime import datetime
from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
import json
from ..log.log import Logger

logger = Logger()


class SearchUser(APIView):
    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return JsonResponse({'status': 404, 'msg': '页面不存在'}, status=404)

    def post(self, request, *args, **kwargs):
        try:
            # 验证是否已登录
            if not request.user.is_authenticated:
                return JsonResponse({'status': 403, 'msg': '未登录'}, status=403)

            # 验证是否为超级管理员
            if not request.user.is_superuser:
                return JsonResponse({'status': 403, 'msg': '权限不足，管理员认证失败'}, status=403)

            # 获取请求数据
            data = json.loads(request.body.decode('utf-8'))
            search_term = data.get('search_term')
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)

            if search_term is None:
                return JsonResponse({'status': 400, 'msg': '未提供查询关键字'}, status=400)

            # SQL 查询
            sql_query = '''
                SELECT * FROM auth_user 
                WHERE id = %s OR username LIKE %s 
                LIMIT %s OFFSET %s
            '''
            count_query = '''
                SELECT COUNT(*) FROM auth_user 
                WHERE id = %s OR username LIKE %s
            '''

            # 参数化查询
            query_params = [search_term, f"%{search_term}%", limit, offset]
            count_params = [search_term, f"%{search_term}%"]

            # 执行 SQL 查询
            with connection.cursor() as cursor:
                # 获取总记录数
                cursor.execute(count_query, count_params)
                total = cursor.fetchone()[0]

                # 获取用户信息
                cursor.execute(sql_query, query_params)
                columns = [col[0] for col in cursor.description]
                users = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # 返回结果
            return JsonResponse({'status': 200, 'total': total, 'data': users}, status=200)

        except Exception as e:
            logger.error(f"{self.request_path(request)}, 服务器错误：{e}")
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)
