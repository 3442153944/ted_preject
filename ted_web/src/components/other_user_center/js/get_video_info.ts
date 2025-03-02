async function get_video_info(id:any):Promise<any>{
    try{
        const response = await fetch('http://localhost:8000/api/video/GetVideoInfo/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            },
            body:JSON.stringify({
                video_id:id
            })
        })
        if(response.ok){
            const data = await response.json();
            return data;
        }
        else{
            const data=await response.json();
            console.warn(data.msg)
            return data;
        }
    }
    catch(e)
    {
        console.log(e);
    }
}

export default get_video_info;