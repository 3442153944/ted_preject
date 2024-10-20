import os
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction, connection
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .log.log import Logger
import json
from django.contrib.auth.hashers import check_password, make_password

logger = Logger()


class EditUserPassword(APIView):
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

    def validate_password(self, password):
        """验证密码是否符合要求：至少8位，包含两种字符"""
        if len(password) < 8:
            return '密码长度不能少于8位'

        # 至少包含两种字符类型：字母、数字、特殊字符
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if sum([has_letter, has_number, has_special]) < 2:
            return '密码至少需要包含字母、数字或特殊字符中的两种'

        return ''

    def post(self, request, *args, **kwargs):
        try:
            # 验证用户是否登录
            if not request.user.is_authenticated:
                return JsonResponse({'status': 401, 'msg': '用户未登录'}, status=401)

            user = request.user
            user_id = user.id

            # 解析请求数据
            data = json.loads(request.body.decode('utf-8'))
            old_password = data.get('old_password', None)
            new_password = data.get('new_password', None)
            confirm_password = data.get('confirm_password', None)

            # 验证旧密码
            if not check_password(old_password, user.password):
                return JsonResponse({'status': 400, 'msg': '旧密码不正确'}, status=400)

            # 验证新密码
            password_error = self.validate_password(new_password)
            if password_error:
                return JsonResponse({'status': 400, 'msg': password_error}, status=400)

            # 确认新密码和确认密码是否一致
            if new_password != confirm_password:
                return JsonResponse({'status': 400, 'msg': '两次输入的新密码不一致'}, status=400)

            # 更新密码
            with transaction.atomic():
                sql='UPDATE auth_user SET password=%s WHERE id=%s'
                with connection.cursor() as cursor:
                    cursor.execute(sql, [make_password(new_password), user_id])
                    if cursor.rowcount == 1:
                        return JsonResponse({'status': 200, 'msg': '密码修改成功'}, status=200)
                    else:
                        raise Exception('修改数量异常')

            logger.info(f'用户 {user.username} 成功修改了密码')

            return JsonResponse({'status': 200, 'msg': '密码修改成功'}, status=200)

        except Exception as e:
            logger.error(f'{self.request_path(request)}, 发生错误：{e}')
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
