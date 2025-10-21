import { useAuth } from "../hooks/useAuth.ts";
import * as React from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const {signup, loading} = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) =>{
        e.preventDefault();
        const ok = await signup(email, password);
        if (ok) navigate("/vault");
    };

    return (
        <div className="auth-container" data-test-selector="auth_container_signup">
            <h2 data-test-selector="signup_label">Sign up</h2>
            <form onSubmit={handleSubmit}>
                <input
                    data-test-selector="email_input"
                    placeholder="Email"
                    value={email}
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
                    {loading ? 'Creating...' : 'Sign Up'}
                </button>
            </form>
        </div>
    );
}