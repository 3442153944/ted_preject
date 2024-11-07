import BaseApi from './base_api'

async function delete_dynamic(id: number) {
    try{
        const response = await BaseApi.post('DeleteDynamic',{'dynamic_id':id})
        return response
    }
    catch(e)
    {
        console.log(e)
    }
}
export default delete_dynamic;