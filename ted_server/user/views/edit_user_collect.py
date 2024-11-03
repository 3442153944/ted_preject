from django.db import connection,transaction,DatabaseError
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger

logger=Logger()

class EditUserCollect(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request_path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self,request,*args,**kwargs):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'status': 401, 'msg': '用户未登录'}, status=401)
            user_id = request.user.id
            data = json.loads(request.body.decode('utf-8'))
            video_id_list = data.get('video_id_list')
            with connection.cursor() as cursor:
                delete_sql='''delete from collect_table where video_id=%s and user_id=%s'''
                for video_id in video_id_list:
                    cursor.execute(delete_sql,(video_id,user_id))
                    if cursor.rowcount==1:
                        return JsonResponse({'status':200,'msg':'取消收藏成功'},status=200)
                    else:
                        raise DatabaseError('数据库修改条数异常，已回滚数据操作')

        except Exception as e:
            logger.error(f'{self.request_path(request)},错误信息为：{e}')
            return JsonResponse({'status':500,'msg':'服务器内部错误'},status=500)