import socket
import time
import random
import threading

# 配置参数
server_ip = "192.168.31.100"
server_port = 12345
data_packet_size = 8096  # 小包数据包大小，1KB
send_interval = 0.00001  # 每秒发送多个数据包
num_threads = 8  # 最大线程数
total_sent = 0
start_time = time.time()

# 创建 UDP 套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 用于发送数据的线程函数
def send_data(thread_id):
    global total_sent
    while True:
        # 模拟生成小数据包
        data = bytearray(random.getrandbits(8) for _ in range(data_packet_size))

        # 记录发送前的时间
        start_send_time = time.time()

        # 发送数据包
        client_socket.sendto(data, (server_ip, server_port))

        # 记录发送后的时间
        end_send_time = time.time()

        # 统计发送的数据量
        total_sent += data_packet_size

        # 打印延迟
        send_delay = end_send_time - start_send_time
        print(f"[Thread-{thread_id}] Sent packet of size {data_packet_size} bytes, delay: {send_delay:.6f} seconds")

        # 计算实时带宽 (以 MB/s 为单位)
        if send_delay > 0:
            bandwidth = data_packet_size / send_delay / 1024 / 1024  # MB/s
            print(f"[Thread-{thread_id}] Real-time bandwidth: {bandwidth:.2f} MB/s")

        # 每秒更新带宽
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            real_time_bandwidth = total_sent / elapsed_time / 1024 / 1024  # MB/s
            print(f"Average real-time bandwidth: {real_time_bandwidth:.2f} MB/s")

        # 每隔一定时间发送一个数据包，保持带宽尽可能高
        time.sleep(send_interval)

# 启动多个线程进行数据发送
def main():
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_data, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print(f"Client started, sending data to {server_ip}:{server_port}")
    main()
