import json
from datetime import datetime
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from ..log.log import Logger
from django.db import connection

logger = Logger()


class Search(APIView):

    def __init__(self):
        super().__init__()
        self.sql_dict = {
            'search_video': '''
            SELECT video_info.id AS video_id, video_info.title AS video_title, video_info.author,
           video_info.author_id, video_info.introduce, video_info.create_time, video_info.tags, 
           video_info.video_file_path, video_info.video_status, video_info.video_cover_path,
           auth_user.id AS user_id, auth_user.introduce, auth_user.user_tags, auth_user.self_website_introduce,
           auth_user.self_website, auth_user.avatar_path, auth_user.username, auth_user.sex, auth_user.top_video,
           (SELECT COUNT(*) FROM watch_table WHERE watch_table.video_id = video_info.id) AS watch_count,
           (SELECT COUNT(*) FROM like_table WHERE like_table.video_id = video_info.id) AS like_count,
           (SELECT COUNT(*) FROM collect_table WHERE collect_table.video_id = video_info.id) AS collect_count
    FROM video_info
    LEFT JOIN auth_user ON auth_user.id = video_info.author_id
    WHERE video_info.title LIKE %s OR video_info.tags LIKE %s
            ''',
            'search_user': '''
           SELECT auth_user.id as user_id, auth_user.username, auth_user.introduce, 
           auth_user.user_tags, auth_user.self_website, 
           auth_user.avatar_path, auth_user.sex
           from auth_user
           where username like %s or user_tags like %s 
            ''',
            'search_user_video':
            '''
            select *,(select count(*) from watch_table where watch_table.video_id=video_info.id) as watch_count,
            (select count(*) from like_table where like_table.video_id=video_info.id) as like_count,
            (select count(*) from collect_table where collect_table.video_id=video_info.id) as collect_count 
             from video_info where author_id=%s
            '''
        }

    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request):
        try:

            data = json.loads(request.body.decode('utf-8'))
            search_key = data.get('search_key', None)
            if search_key and search_key != '' and search_key != ' ':
                search_key = f'%{search_key}%'

                with connection.cursor() as cursor:
                    # 查询视频
                    cursor.execute(self.sql_dict['search_video'], [search_key, search_key])
                    video_data = self.format_data(cursor)

                    # 查询用户
                    cursor.execute(self.sql_dict['search_user'], [search_key, search_key])
                    user_data = self.format_data(cursor)
                    for user in user_data:
                        cursor.execute(self.sql_dict['search_user_video'], [user['user_id']])
                        user['video_data'] = self.format_data(cursor)

                    return JsonResponse({'status': 200, 'msg': '搜索成功', 'video_data': video_data,
                                         'user_data': user_data},status=200)
            else:
                return JsonResponse({'status': 400, 'msg': '搜索关键字为空'}, status=400)

        except Exception as e:
            logger.error(self.request_path(request) + f"错误信息:{e}")
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)

    def format_data(self, cursor):
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchall()
        rows = [dict(zip(columns, row)) for row in result]
        return rows
