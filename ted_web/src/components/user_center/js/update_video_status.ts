async function update_video_status(video_id:any):Promise<any>{
    try{
        const response = await fetch('http://localhost:8000/api/video/UpdateVideoStatus/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            },
            body:JSON.stringify({
                video_id:video_id
            })
        })
        const data = await response.json()
        return data
    }
    catch(e)
    {
        console.log(e)
    }
}
export default update_video_status