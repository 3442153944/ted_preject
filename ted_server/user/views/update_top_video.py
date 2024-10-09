from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction, connection
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .log.log import Logger
import json

logger = Logger()


class UpdateTopVideo(APIView):
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
            # 如果用户已登录
            if request.user.is_authenticated:
                user_id = request.user.id
                data = json.loads(request.body.decode('utf-8'))
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        sql = '''
                        update auth_user set auth_user.top_video=%s where auth_user.id=%s
                        '''
                        edit_type = data.get('edit_type', None)
                        if edit_type is None:
                            return Response({'status': 400, 'msg': '缺少参数edit_type'}, status=400)
                        top_video_id = data.get('top_video_id', None)
                        if edit_type == 'del':
                            top_video_id = None
                            cursor.execute(sql, (top_video_id, user_id))
                            if cursor.rowcount == 1:
                                return Response({'status': 200, 'msg': '删除成功'}, status=200)
                            else:
                                raise Exception('异常更新条数，修改已回退')
                        elif edit_type == 'update':
                            cursor.execute(sql, (top_video_id, user_id))
                            if cursor.rowcount == 1:
                                return Response({'status': 200, 'msg': '更新成功'}, status=200)
                            else:
                                raise Exception('异常更新条数，修改已回退')


        except Exception as e:
            logger.error(f'更新用户信息失败: {str(e)}')
            return Response({'status': 500, 'msg': '更新用户信息失败'}, status=500)
