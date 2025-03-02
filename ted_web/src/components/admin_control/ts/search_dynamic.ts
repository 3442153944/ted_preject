import BaseApi from './base_api'

async function search_dynamic(search_type:any,limit:any,offset:any):Promise<any> {
   try{
        const response = await BaseApi.post('SearchDynamic',{'search_type':search_type,'limit':limit,'offset':offset})
        return response
   }
   catch(error){
       console.log(error)
   }
    
}
export default search_dynamic