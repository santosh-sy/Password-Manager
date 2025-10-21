import { useState } from "react";
import { useAuth } from "../hooks/useAuth.ts";
import { useNavigate } from "react-router-dom";
import * as React from "react";

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const {login , loading} = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const ok = await login(email, password);
        if (ok) navigate("/vault");
    }

    return (
        <div className="auth_contaienr" data-test-selector="auth_container_login">
            <h2 data-test-selector="login_label">Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                    data-test-selector="email_input"
                    placeholder="Email"
                    id="email"
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    data-test-selector="password_input"
                    placeholder="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button
                    type="submit"
                    data-test-selector="login_button"
                    disabled={loading}
                >
                    {loading ? 'Loading...' : 'Login'}
                </button>
            </form>
            <p>Don't have an account?{" "}
                <a href="/signup" style={{ color: "#007bff" }}>
                    Sign up
                </a>
            </p>
        </div>
    )
}