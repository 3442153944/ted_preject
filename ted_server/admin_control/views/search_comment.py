from .BaseApiView import BaseAPIView
from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
import json


class SearchComment(BaseAPIView):
    def post(self, request, *args, **kwargs):
        admin_auth = self.check_admin_permission(request)
        if admin_auth:
            return admin_auth
        try:
            data = json.loads(request.body.decode('utf-8'))
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            search_type = data.get('search_type', None)
            search_type = f'%{search_type}%'
            if search_type is None:
                return JsonResponse({'status': 400, 'msg': '缺少参数'}, status=400)
            with connection.cursor() as cursor:
                search_comment_sql = '''
                select comment_table.id as comm_id,comment_table.video_id as comm_to_video_id,
            comment_table.comment_content ,comment_table.send_user_id as comm_send_time,
             comment_table.reply_comment_id,auth_user.username as username,auth_user.id as user_id,
             auth_user.avatar_path ,video_info.id as video_id,video_info.title as video_title
             from comment_table 
             left join auth_user on auth_user.id=comment_table.send_user_id
             left join video_info on video_info.id=comment_table.video_id
             where comment_table.id like %s or comment_table.comment_content like %s or auth_user.id like %s 
             or auth_user.username like %s or video_info.id like %s or video_info.title like %s 
             limit %s offset %s
                '''
                get_total_sql = '''
                select count(*) from comment_table 
                left join auth_user on auth_user.id=comment_table.send_user_id
                left join video_info on video_info.id=comment_table.video_id
                where comment_table.id like %s or comment_table.comment_content like %s or auth_user.id like %s 
                or auth_user.username like %s or video_info.id like %s or video_info.title like %s 
                '''
                cursor.execute(get_total_sql,
                               [search_type, search_type, search_type, search_type, search_type, search_type])
                total_count = cursor.fetchone()[0]
                cursor.execute(search_comment_sql,
                               [search_type, search_type, search_type, search_type, search_type, search_type, limit,
                                offset])
                result = self.format_result(cursor)
                return JsonResponse({'status': 200, 'msg': 'success', 'data': result, 'total': total_count}, status=200)

        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
