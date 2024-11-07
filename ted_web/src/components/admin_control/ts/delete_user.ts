import BaseAPI from "./base_api"
async function deleteUser(id: any) {
    try {
        const data = await BaseAPI.post('DeleteUser', { 'user_id':id });
        return data;
    } catch (e) {
        console.error("删除用户时出错:", e);
    }
}

export default deleteUser;