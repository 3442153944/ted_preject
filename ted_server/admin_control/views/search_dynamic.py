from .BaseApiView import BaseAPIView
from django.db import connection
from django.http import JsonResponse
import json
from ..log.log import Logger

logger = Logger()


class SearchDynamic(BaseAPIView):
    def post(self, request, *args, **kwargs):
        admin_auth = self.check_admin_permission(request)
        if admin_auth:
            return admin_auth
        try:
            data = json.loads(request.body.decode('utf-8'))
            search_type = data.get('search_type', None)
            search_type = f'%{search_type}%'
            if search_type is None:
                return JsonResponse({'status': 400, 'msg': '缺少参数'}, status=400)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            search_sql = '''
            select dynamic_table.id, title, content, send_user_id, send_time, dynamic_status, img_list,
                auth_user.id as user_id,auth_user.username,auth_user.avatar_path
                from dynamic_table 
                left join auth_user on auth_user.id=dynamic_table.send_user_id
                where dynamic_table.id like %s or dynamic_table.title like %s or auth_user.id LIKE %s 
                or auth_user.username like %s
                limit %s offset %s
            '''
            get_total_count_sql = '''
            select count(*) from dynamic_table 
                left join auth_user on auth_user.id=dynamic_table.send_user_id
                where dynamic_table.id like %s or dynamic_table.title like %s or auth_user.id LIKE %s 
                or auth_user.username like %s
            '''
            with connection.cursor() as cursor:
                cursor.execute(search_sql, [search_type, search_type, search_type, search_type, limit, offset])
                result = self.format_result(cursor)
                cursor.execute(get_total_count_sql, [search_type, search_type, search_type, search_type])
                total_count = cursor.fetchone()[0]
                return JsonResponse({'status': 200, 'msg': 'success', 'data': result, 'total': total_count})

        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
