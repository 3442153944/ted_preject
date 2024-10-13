import io
import os
import json
import shutil
import threading
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.db import connection, transaction, DatabaseError
from django.shortcuts import render
from django.http import JsonResponse
from ..log.log import Logger
from .re_write_img import ReWriteImg
from .reload_video import ReloadVideo
import uuid
from moviepy.editor import VideoFileClip
from .TempChunkFile import TempChunkFile

re_write_img = ReWriteImg()
logger = Logger()
temp_chunk_file = TempChunkFile()
re_load_video = ReloadVideo

class UploadVideo(APIView):
    def __init__(self):
        base_path = os.path.dirname(__file__)
        self.video_save_path = os.path.join(base_path, '../../static/video/')
        self.video_cover_path = os.path.join(base_path, '../../static/img/img/')
        self.video_chunk_temp_path = os.path.join(base_path, '../../static/video/temp/')
        self.temp_chunk_file = [{
            'index': 0
        }]

    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            if not request.user.is_authenticated:
                return JsonResponse({'status': 401, 'msg': '用户未登录'}, status=401)

            cover_file = request.FILES.get('cover')

            #视频封面优先处理并暂存返回临时文件名
            if cover_file:
                re_write_img.set_file(cover_file)
                cover_file = re_write_img.process_image()
                cover_filename = self.generate_unique_filename(self.video_chunk_temp_path)
                self.save_file(os.path.join(self.video_chunk_temp_path, cover_filename + '.png'), cover_file)
                return JsonResponse({'status': 200, 'msg': '作品封面上传成功', 'cover_filename': cover_filename},
                                    status=200)
            video_chunk = request.FILES.get('video_chunk')
            total_chunks = int(request.POST.get('total_chunks'))
            is_end = request.POST.get('is_end')

            #判断临时文件名是否为空，为空则生成，并返回临时文件名到前端
            video_chunk_filename = request.POST.get('video_chunk_filename')
            if video_chunk_filename.trim() == '' or video_chunk_filename is None:
                video_chunk_filename = self.generate_unique_filename(self.video_chunk_temp_path)

                #生成完成后初始化容器
                if temp_chunk_file.init_temp_chunk_file(video_chunk_filename):
                    return JsonResponse({'status': 200, 'msg': '生成分片临时文件名成功',
                                         'video_chunk_filename': video_chunk_filename}, status=200)
                else:
                    return JsonResponse({'status': 500, 'msg': '生成分片临时文件名失败'}, status=500)
            re_try_upload = request.POST.get('re_try_upload', False)
            if re_try_upload == 'true' or re_try_upload == True:
                chunk_index = int(request.POST.get('chunk_index'))
                if temp_chunk_file.update_chunk(video_chunk_filename, chunk_index,
                                                f'{video_chunk_filename}_{chunk_index}',
                                                video_chunk):
                    return JsonResponse({'status': 200, 'msg': '分片重传成功', 'now_index': chunk_index}, status=200)
                return JsonResponse({'status': 500, 'msg': '分片重传失败', 'now_index': chunk_index}, status=500)

            if is_end == 'false' or is_end == False:
                #获取分片索引
                chunk_index = int(request.POST.get('chunk_index'))
                temp_chunk_file.add_chunk(video_chunk_filename, chunk_index,
                                          f'{video_chunk_filename}_{chunk_index}',
                                          video_chunk)
                return JsonResponse({'status': 200, 'msg': '当前分片上传成功',
                                     'now_index': chunk_index}, status=200)
            else:
                file=temp_chunk_file.merge_chunk(video_chunk_filename)
                if file:
                    temp_file=re_load_video.format_video(file)
                    if temp_file:
                        self.save_file(os.path.join(self.video_save_path+f'{video_chunk_filename}.mp4'),temp_file)

                        #获取临时封面的文件名
                        cover_filename=request.POST.get('cover_filename')

                        #从临时文件件中获取封面并剪切到目标文件夹
                        self.cut_file(cover_filename,self.video_chunk_temp_path,self.video_cover_path,cover_filename)
                        data=request.POST.get('video_info',{})
                        with transaction.atomic():
                            self.save_to_database(data,user_id,video_chunk_filename+'.mp4',cover_filename)
                        return JsonResponse({
                            'status': 200,
                            'msg': '视频上传成功',
                            'video_filename': video_chunk_filename,
                            'video_path': video_chunk_filename + '.mp4',
                            'cover_filename': cover_filename+'.png'
                        })

        except Exception as e:
            logger.error(self.request_path(request) + str(e))
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)

    def save_to_database(self, data, user_id, video_filename, cover_filename):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    # 保存文件
    def save_file(self, path, file_content):
        with open(path, 'wb') as f:
            f.write(file_content.getvalue())

    #剪切文件并重命名
    def cut_file(self, filename, source_path, target_path, re_name):
        try:
            # 拼接源文件和目标文件的完整路径
            source_file_path = os.path.join(source_path, filename)
            if re_name is None:
                re_name = filename
            target_file_path = os.path.join(target_path, re_name)

            # 检查源文件是否存在
            if not os.path.exists(source_file_path):
                return f'源文件 {source_file_path} 不存在'

            # 创建目标目录（如果不存在）
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            # 将源文件剪切到目标目录并重命名
            shutil.move(source_file_path, target_file_path)

            return True
        except Exception as e:
            print(e)
            return False


    def generate_unique_filename(self, path):
        while True:
            filename = ''.join([str(i) for i in os.urandom(21)])
            if not os.path.exists(os.path.join(path, filename + '.mp4')) and not os.path.exists(
                    os.path.join(path, filename + '.png')):
                return filename
