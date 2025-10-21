import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const original = error.config;
        if (error.response?.status === 401 && !original._retry) {
            original._retry = true;
            const refresh = localStorage.getItem("refresh_token");
            if (!refresh) throw error;
            try {
                const { data } = await axios.post(`${import.meta.env.VITE_API_URL}/refresh`, refresh, {
                    headers: { "Content-Type": "application/json" },
                });
                localStorage.setItem("access_token", data.access_token);
                api.defaults.headers.common["Authorization"] = `Bearer ${data.access_token}`;
                return api(original);
            } catch {
                localStorage.clear();
                window.location.href = "/login";
            }
        }
        throw error;
    }
)

export default api;