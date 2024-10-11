import os
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection, transaction
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .log.log import Logger
import json
from django.contrib.auth.hashers import check_password, make_password

logger = Logger()

class EditBaseUserInfo(APIView):
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

    def post(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'status': 401, 'msg': '用户未登录'}, status=401)

            user_id = request.user.id
            current_username = request.user.username

            # 解析请求数据
            data = json.loads(request.body.decode('utf-8'))

            # 验证传入的数据
            username = data.get('username', current_username)
            email = data.get('email', None)
            sex = data.get('sex', None)
            birthday = data.get('birthday', None)
            introduce= data.get('introduce', None)
            self_website = data.get('self_website', None)
            self_website_introduce = data.get('self_website_introduce', None)
            user_tags = data.get('user_tags', None)

            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 确保用户名唯一性检查排除当前用户
                    cursor.execute('''SELECT id FROM auth_user WHERE username=%s AND id != %s''', [username, user_id])
                    if cursor.rowcount > 0:
                        return JsonResponse({'status': 400, 'msg': '用户名已存在'}, status=400)

                    # 更新用户信息
                    sql = '''
                    UPDATE auth_user SET username=%s, email=%s, sex=%s, birthday=%s, self_website=%s,
                    self_website_introduce=%s, user_tags=%s,introduce=%s WHERE id=%s
                    '''
                    cursor.execute(sql, [
                        username, email, sex, birthday, self_website,
                        self_website_introduce, user_tags,introduce, user_id
                    ])

                    if cursor.rowcount == 1:
                        return JsonResponse({'status': 200, 'msg': '修改成功'}, status=200)
                    else:
                        raise Exception('异常的修改数量，已回退修改')

        except Exception as e:
            logger.error(f'{self.request_path(request)}, 发生错误：{e}')
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
