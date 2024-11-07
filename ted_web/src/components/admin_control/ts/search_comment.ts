import BaseApi from './base_api'

interface Comment {
    'status':number;
    'data':Array<any>;
    'msg':any;
}

async function search_comment(search_type:any,limit:any,offset:any):Promise<Comment | void> {
    try{
        const response = await BaseApi.post('SearchComment',{'search_type':search_type,'limit':limit,'offset':offset})
        return response
    }
    catch (e){
        console.log(e)
    }
}
export default search_comment