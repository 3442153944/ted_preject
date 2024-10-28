import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection, transaction
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .log.log import Logger

logger = Logger()

class GetOtherUserInfo(APIView):
    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request_path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request):
        try:
            data=json.loads(request.body.decode('utf-8'))
            request_user_id = request.user.id
            user_id = data.get('user_id',None)
            if user_id is None:
                return JsonResponse({'status': 400, 'msg': '参数错误'}, status=400)

            with connection.cursor() as cursor:
                #请求者是否关注了被查询者
                sql='''
                select * from follow_table where operation_user_id=%s and target_user_id=%s and follow_status=1
                '''
                cursor.execute(sql, (request_user_id, user_id))
                is_followed = cursor.fetchone()
                if is_followed:
                    is_followed = 1
                else:
                    is_followed = 0

                # 获取用户的所有信息，不显式排除字段
                sql = '''
                SELECT * FROM auth_user WHERE id = %s
                '''
                cursor.execute(sql, (user_id,))
                user_info = cursor.fetchone()

                if not user_info:
                    return JsonResponse({'status': 404, 'msg': '用户不存在'}, status=404)

                # 获取列名
                columns = [column[0] for column in cursor.description]
                user_data = dict(zip(columns, user_info))

                # 删除密码字段
                user_data.pop('password', None)
                user_data.pop('email',None)

                # 获取用户收藏的视频
                collected_video_sql = '''
                SELECT video_info.*
                FROM collect_table
                JOIN video_info ON collect_table.video_id = video_info.id
                WHERE collect_table.user_id = %s
                '''
                cursor.execute(collected_video_sql, (user_id,))
                collected_videos = cursor.fetchall()
                video_columns = [column[0] for column in cursor.description]
                collected_video_info = [dict(zip(video_columns, video)) for video in collected_videos]

                # 获取用户发布的视频
                user_video_sql = '''
                SELECT * FROM video_info WHERE author_id = %s
                '''
                cursor.execute(user_video_sql, (user_id,))
                user_videos = cursor.fetchall()
                user_video_info = [dict(zip(video_columns, video)) for video in user_videos]
                if user_video_info:
                    watch_sql='''
                    select count(*) from watch_table where video_id=%s
                    '''
                    like_sql='''
                    select count(*) from like_table where video_id=%s
                    '''
                    collect_sql='''
                    select count(*) from collect_table where video_id=%s
                    '''
                    for row in user_video_info:
                        cursor.execute(watch_sql,(row['id'],))
                        row['watch_count']=cursor.fetchone()[0]
                        cursor.execute(like_sql,(row['id'],))
                        row['like_count']=cursor.fetchone()[0]
                        cursor.execute(collect_sql,(row['id'],))
                        row['collect_count']=cursor.fetchone()[0]

                if collected_video_info:
                    watch_sql='''
                    select count(*) from watch_table where video_id=%s
                    '''
                    like_sql='''
                    select count(*) from like_table where video_id=%s
                    '''
                    collect_sql='''
                    select count(*) from collect_table where video_id=%s
                    '''
                    for row in collected_video_info:
                        cursor.execute(watch_sql,(row['id'],))
                        row['watch_count']=cursor.fetchone()[0]
                        cursor.execute(like_sql,(row['id'],))
                        row['like_count']=cursor.fetchone()[0]
                        cursor.execute(collect_sql,(row['id'],))
                        row['collect_count']=cursor.fetchone()[0]

                # 组合数据
                response_data = {
                    'user_info': user_data,
                    'collected_videos': collected_video_info,
                    'user_videos': user_video_info,
                    'is_followed': is_followed
                }

            return JsonResponse({'status': 200, 'msg': '获取成功', 'data': response_data}, status=200)

        except Exception as e:
            logger.error(f'服务器错误: {e}')
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
