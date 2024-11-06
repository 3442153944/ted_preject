async function edit_user_info(user_info:Object, new_password:any):Promise<any> {
    try {
        console.log(localStorage.getItem('auth_token'))
        const response = await fetch('http://localhost:8000/admin/EditUserInfo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({
                user_info: user_info,
                new_password: new_password
            })
        });
        const data = await response.json();
        return data;
    } catch (e) {
        console.log(e);
        return { status: 500, msg: '请求错误' }; // 返回默认错误对象
    }
}

export default edit_user_info;