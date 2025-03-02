from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
import json
from ..log.log import Logger
from django.http import JsonResponse

logger = Logger()


class GetUserList(APIView):
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
            admin_id = request.user.id
            if is_auth:
                with connection.cursor() as cursor:
                    data=json.loads(request.body.decode('utf-8'))
                    limit=data.get('limit', 10)
                    offset=data.get('offset', 0)

                    permission_sql = '''select is_superuser from auth_user where id=%s'''
                    cursor.execute(permission_sql, [admin_id])
                    result = cursor.fetchone()[0]
                    if result not in [1, '1']:
                        return JsonResponse({'status': 403, 'msg': '权限不足'}, status=403)
                    get_user_list_sql = '''
                    select * from auth_user limit %s offset %s
                    '''
                    cursor.execute(get_user_list_sql, [limit, offset])
                    user_list = self.format_result(cursor)
                    total_sql = '''select count(*) from auth_user'''
                    cursor.execute(total_sql)
                    total = cursor.fetchone()[0]
                    return JsonResponse({'status': 200, 'data': user_list,'total':total}, status=200)

        except Exception as e:
            logger.error(self.request_path(request) + str(e))
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)

    def format_result(self, cursor):
        result = cursor.fetchall()
        columns = cursor.description
        rows = [dict(zip([column[0] for column in columns], row)) for row in result]
        return rows
