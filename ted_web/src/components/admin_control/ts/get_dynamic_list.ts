import BaseApi from './base_api'

interface DynamicList{
    'status': number,
    'data': Array<Object>,
    'msg':any
}

async function get_dynamic_list(limit:any,offset:any):Promise<DynamicList|void>{
    try{
        const response = await BaseApi.post('GetDynamicList',{'limit':limit,'offset':offset})
        return response
    }
    catch(error){
        console.log(error)
    }
}
export default get_dynamic_list;