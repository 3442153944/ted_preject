import io
import os
import sys


class TempChunkFile:
    def __init__(self):
        self.temp_mem_disk_path = os.path.join(os.path.dirname(__file__), '../../temp_mem_disk/')
        self.temp_chunk_file = {}
        self.virtual_memory_file_path = os.path.join(self.temp_mem_disk_path, 'virtual.bin')

        # 创建临时磁盘路径，如果不存在
        if not os.path.exists(self.temp_mem_disk_path):
            os.makedirs(self.temp_mem_disk_path)

    # 初始化内存容器
    def init_temp_chunk_file(self, chunk_name):
        if chunk_name not in self.temp_chunk_file:
            self.temp_chunk_file[chunk_name] = []
            return True
        else:
            return False

    # 清空指定容器
    def clear_temp_chunk_file(self, chunk_name):
        if chunk_name in self.temp_chunk_file:
            del self.temp_chunk_file[chunk_name]
            return True
        else:
            return False

    # 向指定容器中添加分片
    def add_chunk(self, chunk_name, chunk_index, chunk_file_name, chunk_file):
        if chunk_name in self.temp_chunk_file:
            if chunk_index is not None and chunk_file_name and chunk_file:
                # 检查当前内存使用情况
                if self.get_memory_usage() < 1 * 1024 * 1024 * 1024:  # 小于 1GB
                    self.temp_chunk_file[chunk_name].append({
                        'chunk_index': chunk_index,
                        'chunk_file_name': chunk_file_name,
                        'chunk_file': chunk_file
                    })
                    self.temp_chunk_file[chunk_name] = sorted(self.temp_chunk_file[chunk_name],
                                                              key=lambda x: x['chunk_index'])
                    return True
                else:
                    # 超过内存限制时，存储到虚拟内存文件
                    self.store_chunk_on_virtual_memory(chunk_name, chunk_index, chunk_file_name, chunk_file)
                    return True
            else:
                return False
        else:
            return False

    # 获取当前内存使用情况
    def get_memory_usage(self):
        # 返回当前进程的内存使用量（字节）
        return sys.getsizeof(self.temp_chunk_file)

    # 将分片存储到虚拟内存文件
    def store_chunk_on_virtual_memory(self, chunk_name, chunk_index, chunk_file_name, chunk_file):
        with open(self.virtual_memory_file_path, 'ab') as f:  # 以附加模式打开
            f.write(chunk_file.getvalue())  # 写入分片内容

    # 修改指定容器中的分片,用户可能的断点续上传
    def update_chunk(self, chunk_name, chunk_index, chunk_file_name, chunk_file):
        if chunk_name in self.temp_chunk_file:
            for chunk_info in self.temp_chunk_file[chunk_name]:
                if chunk_info['chunk_index'] == chunk_index:
                    chunk_info['chunk_file_name'] = chunk_file_name
                    chunk_info['chunk_file'] = chunk_file
                    return True
            return False
        else:
            return False

    # 合并指定容器中的分片并返回合并完成的文件流
    def merge_chunk(self, chunk_name):
        if chunk_name not in self.temp_chunk_file:
            return False

        # 合并文件流
        merged_file = io.BytesIO()
        try:
            # 先处理内存中的分片
            for chunk_info in self.temp_chunk_file[chunk_name]:
                merged_file.write(chunk_info['chunk_file'].getvalue())  # 写入内存中的分片

            # 从虚拟内存文件读取分片
            if os.path.exists(self.virtual_memory_file_path):
                with open(self.virtual_memory_file_path, 'rb') as f:
                    merged_file.write(f.read())

            merged_file.seek(0)  # 将指针重置到文件开头
            return merged_file
        except Exception as e:
            print(e)
            return False
        finally:
            # 合并完成后，清空该容器
            self.clear_temp_chunk_file(chunk_name)

    # 清空虚拟内存文件
    def clear_virtual_memory(self):
        if os.path.exists(self.virtual_memory_file_path):
            os.remove(self.virtual_memory_file_path)
