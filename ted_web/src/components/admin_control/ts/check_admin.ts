async function check_admin():Promise<any> {
    try{
        const response = await fetch('http://localhost:8000/admin/AdminCheck/',{
            method:'post',
            headers:{
                'Content-Type':"application/json",
                'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
            }
        })
        const data = await response.json();
        if(data.status==200){
            return true;
        }
        else{
            return false;
        }
    }
    catch(e)
    {
        console.log(e);
    }
}

export default check_admin;