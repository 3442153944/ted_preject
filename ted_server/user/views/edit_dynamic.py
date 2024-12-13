from datetime import datetime
from django.db import connection,DatabaseError,transaction
from django.http import JsonResponse
from django.shortcuts import render
import json
from rest_framework.views import APIView
from .log.log import Logger
logger = Logger()

class EditDynamic(APIView):
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
                return JsonResponse({'status': 400, 'msg': '未登录'}, status=400)

            user_id = request.user.id
            data=json.loads(request.body.decode('utf-8'))
            dynamic_id=data.get('id',False)
            if dynamic_id:
                delete_sql='''
                delete from dynamic_table where id=%s
                '''
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute(delete_sql,[dynamic_id])
                        if cursor.rowcount==1:
                            return JsonResponse({'status':200,'msg':'删除成功'},status=200)
                        else:
                            raise DatabaseError("异常删除数量，回退修改")

        except Exception as e:
            logger.error(e)
            return JsonResponse({'status':500,'msg':'服务器错误'},status=500)