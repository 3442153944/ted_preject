async function get_video_list(limit:number, offset:number):Promise<any>{
    try{
        const res=await fetch('http://localhost:8000/admin/GetVideoList/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            },
            body:JSON.stringify({
                limit:limit,
                offset:offset
            })
        })
        const data=res.json();
        return data;
    }
    catch(e)
    {
        console.log(e);
        return ({'status':500,'msg':'服务器错误'})
    }
}
export default get_video_list;