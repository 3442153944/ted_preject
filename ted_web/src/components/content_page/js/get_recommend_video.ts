async function get_recommend_video():Promise<any> {
    try{
        const token = localStorage.getItem('auth_token');  // 获取存储的 token
        const res=await fetch('http://localhost:8000/api/video/RecommendVideo/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization': token ? `Bearer ${token}` : ''  // 如果有 token，则使用，否则不添加
            },
            body:JSON.stringify({
                
            })
        })
        if(res.ok){
            const data=res.json();
            return data;
        }
        else{
            const data=res.json();
            console.warn('获取推荐视频失败')
            return data;
        }
    }
    catch (e) {
        console.log(e);
    }
}

export default get_recommend_video;