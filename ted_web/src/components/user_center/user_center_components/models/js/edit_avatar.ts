async function edit_user_avatar(file: File): Promise<any> {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('edit_type', 'avatar'); // 加入 edit_type 字段

        const res = await fetch('http://localhost:8000/api/user/EditUserAvatar/', {
            method: 'post',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            return data;
        } else {
            const data = await res.json();
            console.log('修改用户头像失败');
            return data;
        }
    } catch (e) {
        console.log(e);
    }
}

export default edit_user_avatar;