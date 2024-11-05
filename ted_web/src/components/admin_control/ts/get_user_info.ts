async function get_user_info(){
    try{
        const response= await fetch('http://localhost:8000/api/user/GetUserInfo/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                
            })
        })
        const data= await response.json();
        return data;
    }
    catch(e)
    {
        console.log(e);
    }
}
export default get_user_info;