async function get_watch_his(){
    try{
        const response = await fetch('http://localhost:8000/api/user/GetWatchList/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            }
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