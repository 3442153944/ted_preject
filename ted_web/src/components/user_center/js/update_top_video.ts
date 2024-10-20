async function update_top_video(video_id:any,edit_type:any):Promise<any>{
    try{
        const res=await fetch('http://localhost:8000/api/user/UpdateTopVideo/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${localStorage.getItem('auth_token')}`
            },
            body:JSON.stringify({
                top_video_id:video_id,
                edit_type:edit_type
            })
        })
        if(res.ok)
        {
            const data=await res.json();
            return data;
        }
        else{
            const data=await res.json();
            console.warn('更新置顶视频失败')
            return data;
        }
    }
    catch(e){
        console.log(e)
    }
}

export default update_top_video;