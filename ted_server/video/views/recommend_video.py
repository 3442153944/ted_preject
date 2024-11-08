from django.db import connection
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from datetime import datetime
from ..log.log import Logger
import json
import random

logger = Logger()


class RecommendVideo(APIView):
    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            permission_classes = [AllowAny]  # 允许所有用户访问
            authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]  # 配置认证类
            user_id = request.user.id if request.user.is_authenticated else None

            with connection.cursor() as cursor:
                # 获取所有视频信息
                video_sql = '''
                              SELECT video_info.*, auth_user.username, auth_user.avatar_path,
                                     video_info.id AS video_id  
                              FROM video_info 
                              LEFT JOIN auth_user ON auth_user.id = video_info.author_id
                              '''
                cursor.execute(video_sql)
                result = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                videos = [dict(zip(columns, row)) for row in result]
                # 如果用户已登录，获取用户观看过的视频标签
                if user_id:
                    get_watch_list = '''
                    SELECT video_info.tags 
                    FROM watch_table 
                    LEFT JOIN video_info ON video_info.id = watch_table.video_id
                    WHERE watch_table.user_id = %s
                    '''
                    cursor.execute(get_watch_list, [user_id])
                    watched_tags = cursor.fetchall()

                    # 统计标签出现次数
                    tags_count = {}
                    for row in watched_tags:
                        tags = row[0].split(',') if row[0] else []
                        for tag in tags:
                            if tag in tags_count:
                                tags_count[tag] += 1
                            else:
                                tags_count[tag] = 1

                    # 按标签出现次数降序排序
                    sorted_tags = sorted(tags_count, key=tags_count.get, reverse=True)
                    # 筛选含有高频标签的视频
                    tagged_videos = [video for video in videos if
                                     any(tag in video['tags'].split(',') for tag in sorted_tags)]
                    other_videos = [video for video in videos if video not in tagged_videos]
                    recommended_videos = tagged_videos[:15] + other_videos[:(15 - len(tagged_videos))]
                else:
                    print('未登录用户')
                    # 用户未登录，直接随机选取视频，以视频ID为索引随机选取，不足时从已有的列表中选取
                    #获取ID列表
                    video_ids = [video['video_id'] for video in videos]
                    recommended_videos = []
                    for i in range(15):
                        try:
                            recommended_videos.append(videos[video_ids.index(i)])
                        except:
                            recommended_videos.append(random.choice(videos))
                    print(recommended_videos)

                # 获取每个视频的观看次数
                watch_count_sql = '''
                SELECT COUNT(*) AS watch_count FROM watch_table WHERE video_id = %s
                '''
                for video in recommended_videos:
                    cursor.execute(watch_count_sql, [video['video_id']])
                    video['watch_count'] = cursor.fetchone()[0]
                    video.pop('password', None)
                    video.pop('email', None)
                    video.pop('id', None)
                #print(recommended_videos)

                # 返回推荐视频
                return JsonResponse({'status': 200, 'data': recommended_videos}, status=200)

        except Exception as e:
            logger.error(f'{self.request_path(request)} 错误信息: {e}')
            return Response({'status': 500, 'msg': '服务器错误'}, status=500)
