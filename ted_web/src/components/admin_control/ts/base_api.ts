// ts/base_api.ts
class BaseAPI {
    private baseUrl: string;

    constructor() {
        // 设置基础 URL，后续请求路径在此基础上拼接
        this.baseUrl = 'http://localhost:8000/admin';
    }

    async post(endpoint: string, body: object) {
        try {
            const response = await fetch(`${this.baseUrl}/${endpoint}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify(body)
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error("请求错误:", error);
            throw error; // 可以选择在此处返回特定错误格式
        }
    }
}

export default new BaseAPI();
