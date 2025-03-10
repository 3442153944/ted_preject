from django.db import connection
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from datetime import datetime
from ..log.log import Logger
from django.shortcuts import render
import json
from django.http import JsonResponse

logger = Logger()
class GetVideoInfo(APIView):
    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self,request,*args,**kwargs):
        try:
            permission_classes = [AllowAny]  # 允许所有用户访问
            authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]  # 配置认证类
            data=json.loads(request.body.decode('utf-8'))
            user_id=request.user.id
            video_id=data.get('video_id',False)
            if video_id:
                with connection.cursor() as cursor:
                    sql='''
                    select video_info.id, title,  author_id, video_info.introduce as 'video_introduce',
                     create_time, tags, video_file_path, auth_user.introduce as 'introduce',
                     video_info.video_cover_path,
                    video_status,username,auth_user.introduce,count(watch_table.id) as 'watch_count',
                    count(like_table.id) as 'like_count',count(collect_table.id) as 'collect_count',
                    auth_user.user_tags,auth_user.self_website,auth_user.self_website_introduce,auth_user.avatar_path
                     from video_info left join auth_user on auth_user.id=video_info.author_id
                     left join watch_table on watch_table.video_id =video_info.id
                     left join like_table on like_table.video_id=video_info.id
                     left join collect_table on collect_table.video_id=video_info.id
                     where video_info.id=%s
                     group by auth_user.id,video_info.id
                    '''
                    cursor.execute(sql,[video_id])
                    result=cursor.fetchone()
                    row_dict=dict(zip([column[0] for column in cursor.description],result))
                    is_like_sql='''
                    select * from like_table where video_id=%s and user_id=%s
                    '''
                    cursor.execute(is_like_sql,[video_id,user_id])
                    is_like=cursor.fetchone()
                    row_dict['is_like']=bool(is_like)
                    is_collect_sql='''
                    select * from collect_table where video_id=%s and user_id=%s
                    '''
                    cursor.execute(is_collect_sql,[video_id,user_id])
                    is_collect=cursor.fetchone()
                    row_dict['is_collect']=bool(is_collect)
                    is_follow_sql='''
                    select * from follow_table where follow_status=1 and target_user_id=%s and operation_user_id=%s
                    '''
                    cursor.execute(is_follow_sql,[row_dict['author_id'],user_id])
                    is_follow=cursor.fetchone()
                    row_dict['is_follow']=bool(is_follow)
                    return JsonResponse({'status':200,'msg':'获取成功','data':row_dict},status=200)
            else:
                return JsonResponse({'status':200,'msg':'用户没有发布视频'},status=200)

        except Exception as e:
            logger.error(e)
            return JsonResponse({'status':500,'msg':'服务器错误'},status=500)