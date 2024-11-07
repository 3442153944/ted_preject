import BaseApi from './base_api'

interface comment_list  {
    'status':number;
    'data':Array<any>;
    'msg':any
}

async function get_comment_list(limit:any,offset:any):Promise<comment_list | void>{
    try{
        const response = await BaseApi.post('GetCommentList',{'limit':limit,'offset':offset})
        return response
    }
    catch(error){
        console.log(error)
    }
}
export default get_comment_list