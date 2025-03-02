from rest_framework.views import APIView
from django.db import connection, transaction, DatabaseError
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import json
from ..log.log import Logger
from .BaseApiView import BaseAPIView
logger = Logger()


class DeleteVideo(BaseAPIView):
    def post(self, request, *args, **kwargs):
        is_admin=self.check_admin_permission(request)
        if is_admin:
            return is_admin
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    data = json.loads(request.body.decode('utf-8'))
                    video_id = data.get('video_id', None)
                    if video_id is None:
                        return JsonResponse({'status': 400, 'msg': '参数错误'}, status=400)
                    delete_sql = '''
                    delete from video_info where id=%s
                    '''
                    cursor.execute(delete_sql, [video_id])
                    if cursor.rowcount != 1:
                        raise DatabaseError('异常删除数量，操作已回滚')
                    logger.info(f'{request.user} 删除了视频 {video_id}')
                    return JsonResponse({'status': 200, 'msg': '删除成功'}, status=200)

        except Exception as e:
            logger.error(f"{self.request_path(request)}, 服务器错误：{e}")
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)
