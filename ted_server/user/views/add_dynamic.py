import os
import uuid
import json
from datetime import datetime
from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .log.log import Logger
from .re_write_img import ReWriteImg
import re

re_write_img = ReWriteImg()
logger = Logger()


class AddDynamic(APIView):
    def __init__(self):
        super().__init__()
        self.save_path = os.path.join(os.path.dirname(__file__), '../../static/img/img/')

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
            img_file_list = request.FILES.getlist('img_file')
            format_img_list = self.format_img(img_file_list)

            if not format_img_list:
                return JsonResponse({'status': 400, 'msg': '无有效图像'}, status=400)

            content = self.get_post_content(request)
            title = self.get_post_title(request)

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file_name_list = [self.generate_unique_filename() for _ in format_img_list]

            with transaction.atomic():
                self.insert_dynamic_record(title, content, user_id, now, file_name_list)

                for file_name, file_content in zip(file_name_list, format_img_list):
                    self.save_file(os.path.join(self.save_path, file_name), file_content)

            return JsonResponse({'status': 200, 'msg': '发布成功'}, status=200)

        except Exception as e:
            logger.error(f"{self.request_path(request)}，发生错误，错误信息为：{e}")
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)

    def get_post_content(self, request):
        content = request.POST.get('content')
        if not content:
            raise ValueError('内容不能为空')
        # 使用正则表达式提取 img 标签的 alt 属性
        # 匹配 img 标签并提取 alt 属性
        content = re.sub(r'<img[^>]+alt="([^"]+)"[^>]*>', r'$\1$', content)
        # 剔除可能的危险元素
        content = re.sub(r'<[^>]+>', '', content)
        return content

    def get_post_title(self, request):
        title = request.POST.get('title')
        if not title:
            raise ValueError('标题不能为空')
        return title

    def format_img(self, img_file_list):
        format_img_list = []
        for file in img_file_list:
            re_write_img.set_file(file)
            if not re_write_img.check_file_size():
                logger.warning(f'文件大小超过10M，文件名为：{file.name}')
                return JsonResponse({'status': 400, 'msg': '文件大小超过10M'}, status=400)
            if not re_write_img.is_safe_image():
                logger.warning(f'文件类型不合法，文件名为：{file.name}')
                return JsonResponse({'status': 400, 'msg': '文件类型不合法'}, status=400)

            format_img_list.append(re_write_img.copy_paste())
        return format_img_list

    def generate_unique_filename(self):
        file_name = str(uuid.uuid4())
        return file_name + '.png'

    def insert_dynamic_record(self, title, content, user_id, now, file_name_list):
        with connection.cursor() as cursor:
            sql = '''
                INSERT INTO dynamic_table (title, content, send_user_id, send_time, dynamic_status, img_list) 
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            format_name_list=''
            for file_name in file_name_list:
                format_name_list += file_name + ','
            format_name_list = format_name_list.rstrip(',')
            cursor.execute(sql, [title, content, user_id, now, 1, format_name_list])
            if cursor.rowcount != 1:
                raise Exception('异常的插入条数，已会退修改')

    def save_file(self, path, file_content):
        try:
            # 确保 file_content 是字节流
            if isinstance(file_content, bytes):
                with open(path, 'wb') as f:
                    f.write(file_content)
            else:
                # 如果是 BytesIO 对象，则读取其内容
                with open(path, 'wb') as f:
                    f.write(file_content.getbuffer())  # 使用 getbuffer() 获取字节内容
        except Exception as e:
            logger.error(f'保存文件时发生错误，错误信息为：{e}')
            raise

