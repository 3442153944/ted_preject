async function search(search_key:any):Promise<any> {
    const res=await fetch('http://localhost:8000/api/search/Search/',{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
        },
        body:JSON.stringify({
            search_key:search_key
        })
    })
    const data=await res.json()
    if (res.ok)
    {
        return data
    }
    else{
        console.warn('查询失败')
        console.error(data.msg)
        return data
    }
}

export default search