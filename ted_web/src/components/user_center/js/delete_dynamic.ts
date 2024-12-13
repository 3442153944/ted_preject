async function delete_dynamic(id:any){
    try{
        const res=await fetch('http://localhost:8000/api/user/EditDynamic/',{
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({
                id:id,
            })
        })
        const data=await res.json();
        return data;
    }
    catch(error){
        console.log(error);
    }
}
export default delete_dynamic;