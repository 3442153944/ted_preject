async function update_collect(video_id_list:Array<any>):Promise<any> {
    try{
        const response = await fetch('http://localhost:8000/api/user/EditUserCollect/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            },
            body:JSON.stringify({
                video_id_list:video_id_list
            })
        }
        )
        const data = await response.json()
        return data
    }
    catch(e)
    {
        console.log(e)
    }
}
export default update_collect