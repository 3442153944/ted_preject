async function update_follow_status(target_user_id:any,operation_type:any):Promise<void> {
    try{
        const response = await fetch('http://localhost:8000/api/user/UpdateFollow/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                target_user_id: target_user_id,
                operate_type: operation_type
            })
        })
        if(response.ok){
            const data = await response.json();
            return data;
        }
        else{
            const data = await response.json();
            console.warn(data.msg);
            return data;
        }
    }
    catch (e) {
        console.log(e);
    }
}

export default update_follow_status;