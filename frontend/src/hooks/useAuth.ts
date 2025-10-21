import { useState } from "react";
import api from "../api/api";

export function useAuth() {
    const [loading, setLoading] = useState(false);

    const login = async (email: string, password: string) => {
        setLoading(true);
        try {
            const { data } = await api.post("/auth/login", { email, password });
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            return true;
        } finally {
            setLoading(false);
        }
    };

    const signup = async (email: string, password: string) => {
        setLoading(true);
        try {
            await api.post("/auth/signup", { email, password });
            return await login(email, password);
        } finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        const refresh = localStorage.getItem("refresh_token");
        if (refresh) await api.post("/auth/logout", refresh);
        localStorage.clear();
        window.location.href = "/login";
    };

    return { login, signup, logout, loading };
}
