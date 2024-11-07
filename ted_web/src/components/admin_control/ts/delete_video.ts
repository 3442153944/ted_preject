import BaseApi from './base_api'

async function delete_video(video_id:any):Promise<any>{
    try{
        const response = await BaseApi.post('DeleteVideo',{'video_id':video_id})
        return response
    }
    catch(e)
    {
        console.log(e)
    }
}

export default delete_video;