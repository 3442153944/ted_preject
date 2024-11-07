import BaseApi from './base_api'

async function delete_comment(comment_id: number) {
    try{
        const response = await BaseApi.post('DeleteComment',{'comment_id':comment_id})
        return response
    }
    catch (e) {
        console.log(e)
    }
}

export default delete_comment;