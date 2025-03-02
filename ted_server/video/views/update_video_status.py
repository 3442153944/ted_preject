from rest_framework.views import APIView
from django.db import connection,transaction,DatabaseError
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime
from django.shortcuts import render
import json
import os

logger = Logger()

class UpdateVideoStatus(APIView):
    def __init__(self):
        super().__init__()
        self.static_path='../../static/'
        self.video_path=self.static_path+'video/'
        self.cover_path=self.static_path+'img/img/'

    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'status': 401, 'msg': '用户未登录'}, status=401)
            user_id = request.user.id
            if user_id is None:
                return JsonResponse({'status': 401, 'msg': '用户ID为空，请求参数错误'}, status=401)
            data=json.loads(request.body.decode('utf-8'))
            video_id=data.get('video_id',None)
            if video_id is None:
                return JsonResponse({'status': 400, 'msg': '请求参数错误'}, status=400)
            with transaction.atomic():
                with connection.cursor() as cursor:
                    del_sql='''delete from video_info where video_info.author_id=%s and id=%s'''
                    get_file_name_sql='''select video_file_path,video_cover_path from video_info 
                    where video_info.author_id=%s and id=%s'''
                    video_file_name,video_cover_path=cursor.execute(get_file_name_sql,(user_id,video_id)).fetchone()

                    cursor.execute(del_sql,(user_id,video_id))
                    if cursor.rowcount==1:
                        #删除视频文件
                        with open(self.video_path+video_file_name,'r') as f:
                            os.remove(f.name)
                        #删除封面文件
                        with open(self.cover_path+video_cover_path,'r') as f:
                            os.remove(f.name)
                        return JsonResponse({'status': 200, 'msg': '删除成功'})
                    else:
                        raise  DatabaseError('异常的操作行数，操作已回滚')

        except Exception as e:
            logger.error(f'{self.request_path(request)} 访问出错，错误信息为：{e}')
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)