from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
import json
from ..log.log import Logger
from django.http import JsonResponse

logger = Logger()


class GetVideoList(APIView):
    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            # 验证是否已登录
            if not request.user.is_authenticated:
                return JsonResponse({'status': 403, 'msg': '未登录'}, status=403)

            # 验证是否为超级管理员
            if not request.user.is_superuser:
                return JsonResponse({'status': 403, 'msg': '权限不足，管理员认证失败'}, status=403)

            data = json.loads(request.body.decode('utf-8'))
            limit=data.get('limit',10)
            offset=data.get('offset',0)

            with connection.cursor() as cursor:
                get_video_info_list_sql='''
                select video_info.id as video_id, video_info.title as video_title, video_info.author,
                 video_info.author_id, video_info.introduce as video_introduce,
                 video_info.create_time, video_info.tags as video_tags, video_info.video_file_path,
                  video_info.video_status, 
                 video_info.video_cover_path,auth_user.id as user_id,auth_user.username,auth_user.avatar_path,
                 (select count(*) from watch_table where video_id=video_info.id) as watch_count,
                 (select count(*) from like_table where video_id=video_info.id) as like_count,
                 (select count(*) from collect_table where video_id=video_info.id) as collect_count
                  from video_info 
                left join auth_user on auth_user.id=video_info.author_id 
                limit %s offset %s
                '''
                cursor.execute(get_video_info_list_sql, [limit,offset])
                rows = self.format_result(cursor)
                total_sql='''
                select count(*) from video_info
                '''
                cursor.execute(total_sql)
                total=cursor.fetchone()[0]
                return JsonResponse({'status': 200, 'msg': '获取成功', 'data': rows, 'total': total},status=200)

        except Exception as e:
            logger.error(f"{self.request_path(request)}, 服务器错误：{e}")
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)

    def format_result(self, cursor):
        result = cursor.fetchall()
        columns = cursor.description
        rows = [dict(zip([column[0] for column in columns], row)) for row in result]
        return rows
