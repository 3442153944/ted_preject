from moviepy.editor import VideoFileClip
import ffmpeg
import io
import os

class ReloadVideo:
    def __init__(self, video_file):
        self.video_file = video_file  # 传入的视频文件流

    # 使用 GPU 加速压缩并重新编码视频，返回处理后的文件流
    def format_video(self, bitrate="512k", fps=60):
        try:
            #开始前进行文件校验
            if self.check_video_file() is False:
                return None

            # 创建输入文件的字节流
            input_stream = io.BytesIO(self.video_file.read())

            # 创建输出文件的字节流
            output_stream = io.BytesIO()

            # 将输入字节流转为 FFmpeg 可识别的输入
            input_file = input_stream.getvalue()

            # 调用 FFmpeg 使用 GPU 加速进行视频压缩和重新编码
            process = (
                ffmpeg
                .input('pipe:0')  # 从标准输入读取
                .output('pipe:1', vcodec='h264_nvenc', video_bitrate=bitrate, r=fps, acodec='aac',
                        strict='experimental', pix_fmt='yuv420p')
                .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
            )

            # 写入输入视频流到 FFmpeg
            stdout, _ = process.communicate(input=input_file)

            # 将处理后的字节流写入输出文件流
            output_stream.write(stdout)

            # 重置输出流的指针位置
            output_stream.seek(0)

            # 返回处理后的视频字节流
            return output_stream

        except Exception as e:
            print(f"视频处理时发生错误: {e}")
            return None

    # 进行视频文件格式校验
    def check_video_file(self):
        try:
            # 使用 ffmpeg.probe 进行视频文件内容分析
            self.video_file.seek(0)  # 确保文件流指针在起始位置
            probe = ffmpeg.probe(self.video_file)
            format_info = probe['format']

            # 可以根据需要检查其他信息
            valid_formats = ['mp4', 'avi', 'mkv', 'mov', 'flv', 'wmv', 'webm']
            if format_info['format_name'].split(',')[0] in valid_formats:
                return True
            else:
                print(f"无效的视频格式: {format_info['format_name']}. 只支持: {', '.join(valid_formats)}")
                return False

        except ffmpeg.Error as e:
            print(f"视频文件分析失败: {e.stderr.decode()}")
            return False