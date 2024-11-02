async function upload_video(
    video_file: File,
    video_cover: File,
    video_info: Object,
    progress_callback: (count: number, speed: string, time: string) => void // 新增回调函数
): Promise<any> {
    console.log('开始上传视频...');
    const chunk_size = 1 * 1024 * 1024; // 5 MB
    const total_chunks = Math.ceil(video_file.size / chunk_size);
    let current_chunk = 0;
    let temp_filename = null;
    let cover_filename = null;  // 存储封面图像的临时文件名
    let cover_load_status = false;

    // 上传封面图像
    console.log('正在上传封面图像...');
    do {
        const coverFormData = new FormData();
        coverFormData.append("cover", video_cover, 'cover.jpg');
        const coverResponse = await fetch('http://localhost:8000/api/video/UploadVideo/', {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("auth_token")
            },
            body: coverFormData
        });
        console.log('封面上传响应:', coverResponse);

        if (!coverResponse.ok) {
            console.warn("封面上传失败");
            const data = await coverResponse.json();
            console.log(data);
            return data;
        } else {
            const coverData = await coverResponse.json();
            cover_filename = coverData.cover_filename; // 获取封面临时文件名
            cover_load_status = true;
            console.log("封面上传成功, 临时文件名:", cover_filename);
        }
    } while (false);

    if (cover_load_status) {
        console.log('封面上传成功，开始初始化视频上传...');
        const startTime = Date.now();

        // 初始化视频上传
        const initResponse = await fetch('http://localhost:8000/api/video/UploadVideo/', {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("auth_token")
            },
            body: new URLSearchParams({
                'video_info': JSON.stringify(video_info),
                'is_ok': 'false',
                'temp_filename': ''
            })
        });

        console.log('初始化上传响应:', initResponse);
        if (!initResponse.ok) {
            console.warn("初始化上传失败");
            const data = await initResponse.json();
            return data;
        }

        const initData = await initResponse.json();
        temp_filename = initData.video_chunk_filename;
        console.log('临时文件名:', temp_filename);

        // 上传视频分片
        while (current_chunk < total_chunks) {
            const start = current_chunk * chunk_size;
            const end = Math.min(start + chunk_size, video_file.size);
            const chunk = video_file.slice(start, end);
            const chunkHash = await calculateHash(chunk); // 计算当前分片的哈希

            const formData = new FormData();
            formData.append("video_chunk", chunk);
            formData.append("video_info", JSON.stringify(video_info));
            formData.append("chunk_index", current_chunk.toString());
            formData.append("total_chunks", total_chunks.toString());
            formData.append("is_end", (current_chunk === total_chunks - 1) ? "true" : "false");
            formData.append("video_chunk_filename", temp_filename);
            formData.append("cover_filename", cover_filename); // 将封面文件名附加到每个分片的上传请求
            formData.append("chunk_hash", chunkHash); // 添加哈希值

            const chunkStartTime = Date.now();
            const response = await fetch('http://localhost:8000/api/video/UploadVideo/', {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("auth_token")
                },
                body: formData
            });

            console.log(`第 ${current_chunk + 1} 个分片上传响应:`, response);

            if (!response.ok) {
                console.warn(`第 ${current_chunk + 1} 个分片上传失败`);
                const data = await response.json();
                return data;
            }

            const chunkEndTime = Date.now();
            const chunkDuration = (chunkEndTime - chunkStartTime) / 1000; // 以秒为单位
            const currentSpeed = chunk_size / chunkDuration; 
            const estimatedTime = ((total_chunks - current_chunk - 1) * chunk_size) / currentSpeed; 

            let count = (current_chunk + 1) / total_chunks * 100;
            let speed = (currentSpeed / (1024 * 1024)).toFixed(2);
            let time = estimatedTime.toFixed(0);

            // 调用回调函数，更新前端
            progress_callback(count, speed, time);

            const data = await response.json();
            console.log('分片上传响应:', data);
            current_chunk++;
            if(data.all_success){
                return data;
            }
        }
    } else {
        return '封面上传失败';
    }

    return { status: 200, msg: '所有分片上传成功' };
}


// 计算哈希值
async function calculateHash(fileSlice: Blob): Promise<string> {
    const arrayBuffer = await fileSlice.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex; // 返回哈希值
}

//返回上传进度
function back_upload_progress(count:any,speed:any,time:any){
    return {
        count:count,
        speed:speed,
        time:time
    }
}

export default upload_video;
export {back_upload_progress};
