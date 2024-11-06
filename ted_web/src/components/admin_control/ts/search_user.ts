interface User {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    is_superuser: boolean;
    is_staff: boolean;
    is_active: boolean;
    date_joined: string;
    avatar_path?: string;
    sex?: string;
    birthday?: string;
    introduce?: string;
    self_website?: string;
    self_website_introduce?: string;
    user_tags?: string;
    user_status?: string;
    top_video?: number;
}

interface SearchResponse {
    status: number;
    total: number;
    data: User[];
    msg?: string;
}

async function searchUser(
    searchTerm: string,
    limit: number = 10,
    offset: number = 0
): Promise<SearchResponse | void> {
    try {
        const authToken = localStorage.getItem('auth_token');
        if (!authToken) {
            console.error("Authentication token not found");
            return;
        }

        const response = await fetch('http://localhost:8000/admin/SearchUser/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                search_term: searchTerm,
                limit: limit,
                offset: offset
            })
        });

        if (!response.ok) {
            console.error(`Server error: ${response.status}`);
            return;
        }

        const data: SearchResponse = await response.json();
        return data;

    } catch (error) {
        console.error("An error occurred while searching for users:", error);
    }
}

export default searchUser;
