async function get_video_cover(file: File): Promise<string[]>{
    // 获取视频文件中 5 个不同时间点的帧图像
    const cover_list: string[] = [];
    const video = document.createElement('video');
    video.src = URL.createObjectURL(file);

    // 等待视频元数据加载完成
    await new Promise<void>((resolve) => {
        video.onloadedmetadata = () => resolve();
    });

    // 获取视频总时长
    const duration = video.duration;

    // 随机获取5个时间点的帧
    for (let i = 0; i < 5; i++) {
        const randomTime = Math.random() * duration; // 随机时间点
        video.currentTime = randomTime;

        await new Promise<void>((resolve) => {
            video.onseeked = () => {
                // 创建 canvas 截取当前帧
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                if (ctx) {
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    cover_list.push(canvas.toDataURL('image/jpeg'));
                    resolve();
                }
                else {
                    console.error('Failed to get video cover');
                }
            };
        });
    }
    //删除video元素
    video.remove();
    return cover_list;
}

export default get_video_cover;