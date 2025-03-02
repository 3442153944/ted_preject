async function get_user_list(limit=10,offset=0){
    try{
        const response = await fetch('http://localhost:8000/admin/GetUserList/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${localStorage.getItem('auth_token')}`
            },
            body:JSON.stringify({
                limit:limit,
                offset:offset
            })
        })
        const data = await response.json();
        return data;
    }catch(e){
        console.log(e);
    }
}
export default get_user_list;