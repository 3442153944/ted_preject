import hashlib
import io
import os
import psutil
import threading
import subprocess
from moviepy.editor import VideoFileClip


class TempChunkFile:
    def __init__(self):
        self.temp_chunk_file = {}
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.merging = {}
        self.target_path =''

    def init_temp_chunk_file(self, chunk_name,target_path):
        with self.lock:
            if chunk_name not in self.temp_chunk_file:
                self.temp_chunk_file[chunk_name] = []
                target_path = os.path.join(target_path, chunk_name+'.part')
                print(chunk_name, '初始化成功')
                return True
            else:
                return False

    def clear_temp_chunk_file(self, chunk_name):
        with self.lock:
            if chunk_name in self.temp_chunk_file:
                del self.temp_chunk_file[chunk_name]
                print(chunk_name, '清空成功')
                return True
            else:
                return False

    def validate_video_file(self, chunk_file):
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "null", "/dev/null"],
            input=chunk_file.read(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0

    def add_chunk(self, chunk_name, chunk_index, chunk_file_name, chunk_file, chunk_hash):
        if not self.validate_video_file(chunk_file):
            print(f"分片 {chunk_file_name} 不是有效的视频文件.")
        if self.validate_chunk_hash(chunk_file, chunk_hash):
            print(chunk_name, f'分片 {chunk_file_name} 验证通过.')
        else:
            print(chunk_name, f'分片 {chunk_file_name} 验证失败.')

        with self.lock:
            if chunk_name in self.temp_chunk_file:
                chunk_file.seek(0, os.SEEK_END)
                chunk_size = chunk_file.tell()
                chunk_file.seek(0)

                chunk_data = io.BytesIO(chunk_file.read())
                self.temp_chunk_file[chunk_name].append({
                    'chunk_index': chunk_index,
                    'chunk_file': chunk_data
                })
                self.temp_chunk_file[chunk_name] = sorted(self.temp_chunk_file[chunk_name],
                                                          key=lambda x: x['chunk_index'])
                print(chunk_name, f'添加分片成功,分片索引为:{chunk_index}')
                return True
            else:
                return False

    def validate_chunk_hash(self, chunk_file, chunk_hash):
        chunk_file.seek(0)  # 确保从开头读取
        sha256 = hashlib.sha256()
        while chunk := chunk_file.read(4096):
            sha256.update(chunk)
        computed_hash = sha256.hexdigest()
        return computed_hash == chunk_hash

    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        print('当前内存使用情况:', memory_info.rss)
        return memory_info.rss

    def merge_chunk(self, chunk_name):
        with self.condition:
            if chunk_name not in self.temp_chunk_file:
                print(chunk_name, '容器不存在')
                return False

            if self.merging.get(chunk_name, False):
                print(chunk_name, '正在合并，等待合并完成...')
                self.condition.wait_for(lambda: not self.merging.get(chunk_name, False), timeout=30)
                if self.merging.get(chunk_name, False):
                    print(chunk_name, '合并超时')
                    return False

            self.merging[chunk_name] = True

        merged_file = io.BytesIO()
        try:
            with self.lock:
                # 按索引从小到大排序
                self.temp_chunk_file[chunk_name] = sorted(self.temp_chunk_file[chunk_name],
                                                          key=lambda x: x['chunk_index'])
                print(self.temp_chunk_file)
                print(self.temp_chunk_file[chunk_name])
                # 拼接字节流
                for chunk in self.temp_chunk_file[chunk_name]:
                    merged_file.write(chunk['chunk_file'].getvalue())

                merged_file.seek(0)

                # 使用 MoviePy 验证合并后的字节流
                if not self.validate_merged_file(merged_file):
                    print('合并后的文件无效.')

                print(chunk_name, '合并完成')
                self.clear_temp_chunk_file(chunk_name)

                return merged_file  # 返回合并后的字节流
        except Exception as e:
            print(f'合并过程发生错误: {e}')
            return False
        finally:
            with self.condition:
                self.merging[chunk_name] = False
                self.condition.notify_all()

    def validate_merged_file(self, merged_file):
        try:
            merged_file.seek(0)
            VideoFileClip(merged_file).close()
            return True
        except Exception as e:
            print(f'合并验证失败: {e}')
            return False
