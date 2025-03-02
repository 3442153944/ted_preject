from .BaseApiView import BaseAPIView
from django.db import connection
from django.http import JsonResponse
import json
from ..log.log import Logger

logger = Logger()


class GetCommentList(BaseAPIView):
    def post(self, request, *args, **kwargs):
        try:
            admin_auth = self.check_admin_permission(request)
            if admin_auth:
                return admin_auth
            data = json.loads(request.body.decode('utf-8'))
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)

            get_comment_list_sql = '''
            select comment_table.id as comm_id,comment_table.video_id as comm_to_video_id,
            comment_table.comment_content ,comment_table.send_user_id as comm_send_time,
             comment_table.reply_comment_id,auth_user.username as username,auth_user.id as user_id,
             auth_user.avatar_path ,video_info.id as video_id,video_info.title as video_title,
             comment_table.send_time as comm_send_time
             from comment_table 
             left join auth_user on auth_user.id=comment_table.send_user_id
             left join video_info on video_info.id=comment_table.video_id
             limit %s offset %s
            '''
            get_total_count_sql = '''
            select count(comment_table.id) as total_count from comment_table
            '''
            with connection.cursor() as cursor:
                cursor.execute(get_comment_list_sql, (limit, offset))
                result = self.format_result(cursor)
                cursor.execute(get_total_count_sql)
                total = cursor.fetchone()[0]
                return JsonResponse({'status': 200, 'msg': '获取评论列表成功', 'data': result, 'total': total},
                                    status=200)

        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
