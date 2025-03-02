import BaseApi from './base_api'

async function search_video(search_type:any,limit:any,offset:any){
    try{
        const response = await BaseApi.post('SearchVideo',{'search_type':search_type,'limit':limit,'offset':offset})
        return response
    }
    catch(error){
        console.log(error)
    }
}

export default search_video