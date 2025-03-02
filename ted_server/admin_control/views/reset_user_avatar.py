from datetime import datetime
from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
import json
from ..log.log import Logger

logger = Logger()

class ResetUserAvatar(APIView):
    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self,request, *args, **kwargs):
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            is_auth = request.user.is_authenticated
            admin_id = request.user.id

            if not is_auth:
                return JsonResponse({'status': 403, 'msg': '未登录'}, status=403)
            data=json.loads(request.body.decode('utf-8'))
            user_id = data.get('id', None)
            if user_id is None:
                return JsonResponse({'status': 400, 'msg': '参数错误'}, status=400)
            # 使用事务确保数据一致性
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 检查是否为超级管理员
                    is_super_sql = 'SELECT is_superuser FROM auth_user WHERE id=%s'
                    cursor.execute(is_super_sql, (admin_id,))
                    result = cursor.fetchone()

                    if not result or result[0] not in [1, '1']:
                        return JsonResponse({'status': 403, 'msg': '权限不足'}, status=403)

                    reset_avatar_sql = 'UPDATE auth_user SET avatar_path=%s WHERE id=%s'
                    cursor.execute(reset_avatar_sql, ('default_avatar', user_id))
                    if cursor.rowcount != 1:
                        raise  DatabaseError('异常更新条数，已回退修改')
                    return JsonResponse({'status': 200, 'msg': '重置成功'}, status=200)


        except DatabaseError as db_err:
            logger.error(f"{self.request_path(request)}, 数据库错误：{db_err}")
            return JsonResponse({'status': 500, 'msg': '数据库错误，修改失败'}, status=500)

        except Exception as e:
            logger.error(f"{self.request_path(request)}, 服务器错误：{e}")
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)