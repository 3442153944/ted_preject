async function get_all_user_info(user_id:any):Promise<any> {
    try{
        const response=await fetch('http://localhost:8000/api/user/GetOtherUserInfo/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${localStorage.getItem('auth_token')}`
            },
            body:JSON.stringify({
                user_id:user_id
            })
        })
        if (response.ok){
            const data=await response.json();
            return data;
        }
        else{
            const data=await response.json();
            console.warn(data.msg);
            return data;
        }
    }
    catch (error) {
        console.log(error);
    }
}

export default get_all_user_info;