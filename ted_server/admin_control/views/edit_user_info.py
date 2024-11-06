from datetime import datetime
from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
import json
from ..log.log import Logger

logger = Logger()


class EditUserInfo(APIView):
    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            is_auth = request.user.is_authenticated
            admin_id = request.user.id

            if not is_auth:
                return JsonResponse({'status': 403, 'msg': '未登录'}, status=403)

            data = json.loads(request.body.decode('utf-8'))

            user_info = data.get('user_info', {})
            if not user_info:
                return JsonResponse({'status': 400, 'msg': '未提供用户信息'}, status=400)
            user_id = user_info.get('id')
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

                    # 更新用户信息
                    edit_sql = '''
                    UPDATE auth_user SET username=%s, email=%s, user_tags=%s, introduce=%s,
                    is_superuser=%s, sex=%s, self_website=%s, self_website_introduce=%s,
                    date_joined=%s WHERE id=%s
                    '''

                    # 更新用户信息
                    cursor.execute(
                        edit_sql,
                        (
                            user_info.get('username', ''),
                            user_info.get('email', ''),
                            user_info.get('user_tags', ''),
                            user_info.get('introduce', ''),
                            user_info.get('is_superuser', 0),
                            user_info.get('sex', '未知'),
                            user_info.get('self_website', ''),
                            user_info.get('self_website_introduce', ''),
                            user_info.get('date_joined', now),
                            user_id
                        )
                    )

                    if cursor.rowcount != 1:
                        raise DatabaseError('用户信息修改失败，已回退')

                    # 若提供了新密码，则更新密码
                    new_password = data.get('new_password')
                    if new_password:
                        update_password_sql = 'UPDATE auth_user SET password=%s WHERE id=%s'
                        cursor.execute(update_password_sql, (make_password(new_password), user_id))
                        if cursor.rowcount != 1:
                            raise DatabaseError('密码修改失败，已回退')
                        logger.info(f'{admin_id}在{now}修改了{user_id}的密码')

                    logger.info(f'{admin_id}在{now}修改了{user_id}的信息')

                    # 成功响应
                    return JsonResponse({'status': 200, 'msg': '修改成功'}, status=200)

        except DatabaseError as db_err:
            logger.error(f"{self.request_path(request)}, 数据库错误：{db_err}")
            return JsonResponse({'status': 500, 'msg': '数据库错误，修改失败'}, status=500)

        except Exception as e:
            logger.error(f"{self.request_path(request)}, 服务器错误：{e}")
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)
