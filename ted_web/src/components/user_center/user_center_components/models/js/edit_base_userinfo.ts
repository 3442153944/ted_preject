async function edit_base_userinfo(username: string, email: string, sex: string, birthday: string,introduce:string, self_website: string,
    self_website_introduce: string, user_tags: string
) {
    try {
        const res = await fetch('http://localhost:8000/api/user/EditBaseUserInfo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                username: username,
                email: email,
                sex: sex,
                birthday: birthday,
                introduce: introduce,
                self_website: self_website,
                self_website_introduce: self_website_introduce,
                user_tags: user_tags
            })
        })
        if (res.ok) {
            const data = await res.json()
            return data
        }
        else {
            const data = await res.json()
            console.warn('更新信息失败')
            return data
        }
    }
    catch (e) {
        console.log(e)
    }
}
export default edit_base_userinfo