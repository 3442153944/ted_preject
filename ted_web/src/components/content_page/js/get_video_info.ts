async function get_video_info(video_id: any) {
    try{
        const token=localStorage.getItem('auth_token')
        const res=await fetch('http://localhost:8000/api/video/GetVideoInfo/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''  // 如果有 token，则使用，否则不添加
            },
            body: JSON.stringify({
                video_id: video_id
            })
        })
        if(res.ok){
            const data=await res.json();
            return data
        }
        else{
            const data=await res.json();
            console.warn('获取视频信息失败')
            return data
        }
    }
    catch(error) {
        console.log(error);
    }
}

export default get_video_info