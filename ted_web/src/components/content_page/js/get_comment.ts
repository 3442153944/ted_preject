async function get_comment_list(video_id: any, limit: any, offset: any): Promise<any> {
    try {
        const token= localStorage.getItem('auth_token')
        const res = await fetch('http://localhost:8000/api/comment/GetComment/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''  // 如果有 token，则使用，否则不添加
            },
            body: JSON.stringify({
                video_id: video_id,
                limit: limit,
                offset: offset
            })
        })
        if (res.ok) {
            const data = await res.json();
            return data;
        }
        else {
            return false;
        }
    }
    catch (e) {
        console.log(e)
    }
}

async function get_reply_comment_list(video_id: any, reply_comment_id:any,limit: any, offset: any): Promise<any> {
    try {
        const token= localStorage.getItem('auth_token')
        const res = await fetch('http://localhost:8000/api/comment/GetReplyComment/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''  // 如果有 token，则使用，否则不添加
            },
            body: JSON.stringify({
                video_id: video_id,
                reply_comment_id: reply_comment_id,
                limit: limit,
                offset: offset
            })
        })
        if (res.ok) {
            const data = await res.json();
            return data;
        }
        else {
            return false;
        }
    }
    catch (e) {
        console.log(e)
    }
}

export { get_comment_list ,get_reply_comment_list}