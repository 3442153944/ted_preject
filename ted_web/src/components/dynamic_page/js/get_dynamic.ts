async function get_dynamic(user_id:any,request_type:any,
    self_limit:any,self_offset:any,other_limit:any,other_offset:any):Promise<any> {
    try{
        const response = await fetch('http://localhost:8000/api/user/GetDynamicList/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            },
            body:JSON.stringify({
                user_id:user_id,
                request_type:request_type,
                self_limit:self_limit,
                self_offset:self_offset,
                other_limit:other_limit,
                other_offset:other_offset
            })
        })
        if (response.ok){
            const data = await response.json()
            return data
        }
        else{
            const data = await response.json()
            console.warn(data.msg)
            return data
        }
    }
    catch(e)
    {
        console.log(e)
    }
}
export default get_dynamic