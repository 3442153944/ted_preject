async function upload_video(video_file: File, video_cover: File, video_info: Object): Promise<any> {
    const chunk_size = 1024 * 1024; // 1 MB
    const total_chunks = Math.ceil(video_file.size / chunk_size);
    let current_chunk = 0;
    let temp_filename = null;

    // 第一次上传，生成临时文件名
    const initResponse = await fetch('http://localhost:8000/api/video/UploadVideo/', {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("auth_token")
        },
        body: new URLSearchParams({
            'video_info': JSON.stringify(video_info),
            'is_ok': 'false', // 这只是为了请求生成 temp_filename
            'temp_filename': '' // 第一次上传不需要传递
        })
    });

    if (!initResponse.ok) {
        console.warn("初始化上传失败");
        const data = await initResponse.json();
        return data;
    }

    const initData = await initResponse.json();
    temp_filename = initData.temp_filename; // 从响应中获取临时文件名

    // 上传视频分片
    while (current_chunk < total_chunks) {
        const start = current_chunk * chunk_size;
        const end = Math.min(start + chunk_size, video_file.size);
        const chunk = video_file.slice(start, end);

        const formData = new FormData();
        formData.append("chunk", chunk);
        formData.append("video_info", JSON.stringify(video_info));
        formData.append("chunk_index", current_chunk.toString());
        formData.append("total_chunks", total_chunks.toString());
        formData.append("is_ok", (current_chunk == total_chunks - 1) ? "true" : "false"); // 最后一个分片设置is_ok为true
        formData.append("temp_filename", temp_filename); // 始终使用同一个 temp_filename

        const response = await fetch('http://localhost:8000/api/video/UploadVideo/', {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("auth_token")
            },
            body: formData
        });

        if (!response.ok) {
            console.warn(`第 ${current_chunk + 1} 个分片上传失败`);
            const data = await response.json();
            return data;
        }

        current_chunk++;
    }

    // 上传封面图像
    const coverFormData = new FormData();
    coverFormData.append("cover", video_cover);
    const coverResponse = await fetch('http://localhost:8000/api/video/UploadVideo/', {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("auth_token")
        },
        body: coverFormData
    });

    if (!coverResponse.ok) {
        console.warn("封面上传失败");
        const data = await coverResponse.json();
        return data;
    }

    // 返回最终上传的结果
    return { status: 200, msg: '所有分片上传成功' };
}

export default upload_video;
