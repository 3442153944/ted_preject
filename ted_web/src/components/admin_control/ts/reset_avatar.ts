async function reset_avatar(id:any){
    try{
        const response = await fetch('http://localhost:8000/admin/ResetUserAvatar/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({
                id: id
            })
        })
        const data = await response.json();
        return data;
    }
    catch(err){
        console.log(err);
        return {'status':500,'msg':'服务器错误'}
    }
}

export default reset_avatar;