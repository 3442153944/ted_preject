import os
import json
from datetime import datetime
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from ..log.log import Logger
from .re_write_img import ReWriteImg
from .append_file import AppendFile
from django.db import connection,transaction,DatabaseError

re_write_img = ReWriteImg()
logger = Logger()

class UploadVideo(APIView):
    def __init__(self):
        super().__init__()
        base_path = os.path.dirname(__file__)
        self.video_save_path = os.path.join(base_path, '../../static/video/')
        self.video_chunk_temp_path = os.path.join(base_path, '../../static/video/temp/')
        self.video_cover_path = os.path.join(base_path, '../../static/img/img/')
        self.append_file_handler = AppendFile()  # 使用 AppendFile 类来处理文件

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

            # 封面处理
            cover_file = request.FILES.get('cover')
            if cover_file:
                print('开始处理封面')
                re_write_img.set_file(cover_file)
                cover_file = re_write_img.copy_paste()
                cover_filename = self.generate_unique_filename(self.video_chunk_temp_path)
                self.save_file(os.path.join(self.video_chunk_temp_path, cover_filename + '.png'), cover_file)
                return JsonResponse({'status': 200, 'msg': '作品封面上传成功', 'cover_filename': cover_filename},
                                    status=200)

            # 视频处理
            video_chunk = request.FILES.get('video_chunk')
            is_end = request.POST.get('is_end')
            video_chunk_filename = request.POST.get('video_chunk_filename')

            # 如果是新的视频分片，则初始化文件路径
            if not video_chunk_filename:
                video_chunk_filename = self.generate_unique_filename(self.video_chunk_temp_path)
                temp_file_path = os.path.join(self.video_chunk_temp_path, video_chunk_filename + '.part')
                return JsonResponse(
                    {'status': 200, 'msg': '生成分片临时文件名成功', 'video_chunk_filename': video_chunk_filename},
                    status=200)

            # 处理分片
            chunk_index = int(request.POST.get('chunk_index', 0))
            chunk_hash = request.POST.get('chunk_hash', None)
            temp_file_path = os.path.join(self.video_chunk_temp_path, video_chunk_filename + '.part')

            # 将视频分片追加写入
            self.append_file_handler.append_file(temp_file_path, chunk_hash, video_chunk)

            if is_end in ['true', True]:
                cover_filename = request.POST.get('cover_filename')
                data = json.loads(request.POST.get('video_info'))
                # 合并完成，修改后缀并返回
                final_file_path = os.path.join(self.video_save_path, video_chunk_filename + '.mp4')
                self.append_file_handler.complete_file(temp_file_path, final_file_path)

                # 移动封面文件到目标文件夹
                cover_src_path = os.path.join(self.video_chunk_temp_path, cover_filename + '.png')
                cover_dest_path = os.path.join(self.video_cover_path, cover_filename + '.png')
                self.move_file(cover_src_path, cover_dest_path)

                # 保存到数据库
                self.save_to_database(data, request.user.id, video_chunk_filename, cover_filename)
                return JsonResponse({
                    'status': 200,
                    'msg': '视频上传成功',
                    'video_filename': video_chunk_filename,
                    'video_path': final_file_path,
                    'cover_filename': cover_filename,
                    'data': data
                }, status=200)

            return JsonResponse({'status': 200, 'msg': '当前分片上传成功', 'now_index': chunk_index}, status=200)

        except Exception as e:
            logger.error(self.request_path(request) + str(e))
            print(e)
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)

    def save_to_database(self, data, user_id, video_filename, cover_filename):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO video_info 
                    (title, author, author_id, introduce, create_time, tags, 
                    video_file_path, video_status, video_cover_path) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', [
                    data.get('title', '未命名'),
                    data.get('author', ''),
                    user_id,
                    data.get('introduce', ''),
                    now,
                    data.get('tags', ''),
                    (video_filename + '.mp4'),
                    1,
                    cover_filename
                ])
                if cursor.rowcount != 1:
                    raise DatabaseError('插入数据条数错误，已回滚操作')
                return True
        except Exception as e:
            print(e)
            return JsonResponse({'status':500,'msg':'插入数据时发生错误'},status=200)

    # 保存文件
    def save_file(self, path, file_content):
        with open(path, 'wb') as f:
            f.write(file_content.read())
            print('保存文件,保存路径为：', path)

    def generate_unique_filename(self, path):
        while True:
            filename = ''.join([str(i) for i in os.urandom(21)])
            if not os.path.exists(os.path.join(path, filename + '.mp4')) and not os.path.exists(
                    os.path.join(path, filename + '.png')):
                return filename

    # 移动文件
    def move_file(self, src_path, dest_path):
        if os.path.exists(src_path):
            os.rename(src_path, dest_path)
            print(f'封面文件已从 {src_path} 移动到 {dest_path}')
        else:
            print(f'封面文件 {src_path} 不存在')
