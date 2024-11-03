from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger

logger = Logger()


def format_result(cursor):
    result = cursor.fetchall()
    columns = cursor.description
    rows = [dict(zip([column[0] for column in columns], row)) for row in result]
    return rows


class GetWatchList(APIView):

    def log_request(self, request, user_info=""):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f'{request_ip} 在 {now} 访问了 {request_path}'
        if user_info:
            log_message += f" 用户: {user_info}"
        logger.warning(log_message)

    def get(self, request):
        self.log_request(request, str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 403, 'msg': '未登录'}, status=403)

        user_id = request.user.id
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 查询观看记录
                    watch_history_sql = '''
                    SELECT 
                        watch_table.id AS watch_his_id, 
                        watch_table.video_id AS watch_his_video_id,
                        watch_table.watch_time AS watch_his_time,
                        video_info.author_id, 
                        video_info.title, 
                        video_info.video_cover_path,
                        video_info.video_file_path,
                        (select count(*) from watch_table where watch_table.video_id=video_info.id) as watch_count,
                        (select count(*) from like_table where like_table.video_id=video_info.id) as like_count,
                        (select count(*) from collect_table where collect_table.video_id=video_info.id) as collect_count,
                        video_info.introduce
                    FROM 
                        watch_table
                    LEFT JOIN 
                        video_info ON video_info.id = watch_table.video_id
                    WHERE 
                        watch_table.user_id = %s
                    '''
                    cursor.execute(watch_history_sql, [user_id])
                    watch_history = format_result(cursor)

                    # 获取所有相关作者信息
                    author_ids = list(set(row['author_id'] for row in watch_history))
                    if author_ids:
                        authors_sql = '''
                        SELECT id, avatar_path, username 
                        FROM auth_user 
                        WHERE id IN %s
                        '''
                        cursor.execute(authors_sql, [tuple(author_ids)])
                        authors_info = {author['id']: author for author in format_result(cursor)}

                        # 将作者信息加入到观看记录中
                        for record in watch_history:
                            record['author_info'] = authors_info.get(record['author_id'], {})

                return JsonResponse({'status': 200, 'msg': '获取成功', 'data': watch_history})

        except Exception as e:
            print(e)
            self.log_request(request, f"错误信息为: {e}")
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)
