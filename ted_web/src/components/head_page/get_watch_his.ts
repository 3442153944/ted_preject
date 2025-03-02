async function get_watch_his(limit=10,offset=0):Promise<any>{
    try{
        const response = await fetch('http://localhost:8000/api/user/GetWatchList/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            },
            body:JSON.stringify({
                limit:limit,
                offset:offset
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
export default get_watch_his