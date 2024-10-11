async function edit_password(old_password:string,new_password:string,confirm_password:string){
    try{
        const res=await fetch('http://localhost:8000/api/user/EditUserPassword/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('auth_token')
            },
            body:JSON.stringify({
                old_password:old_password,
                new_password:new_password,
                confirm_password:confirm_password
            })
        })
        if(res.ok)
        {
            const data=await res.json();
            return data;
        }
        else{
            const data=await res.json();
            console.warn('修改密码失败')
            return data;
        }
    }
    catch(error){
        console.log(error);
    }
}
export default edit_password;