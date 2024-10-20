import hashlib
import os
import time

class AppendFile:
    def append_file(self, target_path, chunk_hash, chunk_file):
        """追加方式写入视频文件片段."""
        print(f"准备追加文件到: {target_path}")  # 调试打印
        if self.check_hash(chunk_hash, chunk_file):
            retry_count = 5  # 设置重试次数
            chunk_file.seek(0)
            for attempt in range(retry_count):
                try:
                    with open(target_path, 'ab') as f:
                        f.write(chunk_file.read())
                    print(f"分片已成功追加到 {target_path}.")
                    return
                except PermissionError:
                    print(f"追加文件时权限被拒绝: {target_path}")
                    if attempt < retry_count - 1:
                        print("稍后重试...")
                        time.sleep(1)
                except Exception as e:
                    print(f"追加文件时发生其他错误: {e}")
        else:
            print("分片哈希校验失败，未追加.")

    def check_hash(self, chunk_hash, chunk_file):
        """哈希校验 SHA-256。"""
        chunk_file.seek(0)
        sha256 = hashlib.sha256()
        while chunk := chunk_file.read(4096):
            sha256.update(chunk)
        computed_hash = sha256.hexdigest()
        return computed_hash == chunk_hash

    def complete_file(self, temp_file_path, final_file_path):
        """更正后缀为 .mp4 完成合并。"""
        retry_count = 5  # 设置重试次数
        for attempt in range(retry_count):
            try:
                os.rename(temp_file_path, final_file_path)
                print(f"文件已重命名为: {final_file_path}")
                return True
            except PermissionError:
                print("文件正在使用中，稍后重试...")
                time.sleep(1)
            except Exception as e:
                print(f"重命名文件失败: {e}")
                return False
        return False
