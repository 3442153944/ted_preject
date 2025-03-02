from .BaseApiView import BaseAPIView
from django.db import connection
from django.http import JsonResponse
import json
from ..log.log import Logger

logger = Logger()


class GetDynamicList(BaseAPIView):
    def post(self, request, *args, **kwargs):
        admin_auth = self.check_admin_permission(request)
        if admin_auth:
            return admin_auth
        try:
            data = json.loads(request.body.decode('utf-8'))
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            with connection.cursor() as cursor:
                get_dynamic_list_sql = """
                select dynamic_table.id, title, content, send_user_id, send_time, dynamic_status, img_list,
                auth_user.id as user_id,auth_user.username,auth_user.avatar_path
                from dynamic_table 
                left join auth_user on auth_user.id=dynamic_table.send_user_id
                limit %s offset %s
                """
                get_total_count_sql = """
                select count(*) from dynamic_table
                """
                cursor.execute(get_dynamic_list_sql, (limit, offset))
                dynamic_list = self.format_result(cursor)
                cursor.execute(get_total_count_sql)
                total_count = cursor.fetchone()[0]
                return JsonResponse({'status': 200, 'msg': 'success', 'data': dynamic_list, 'total': total_count})
        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
