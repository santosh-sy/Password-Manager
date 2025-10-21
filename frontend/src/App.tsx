import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Vault from "./components/Vault";

export default function App() {
    const isAuthenticated = !!localStorage.getItem("access_token");

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/vault" element={isAuthenticated ? <Vault /> : <Navigate to="/login" />} />
                <Route path="*" element={<Navigate to={isAuthenticated ? "/vault" : "/login"} />} />
            </Routes>
        </BrowserRouter>
    );
}
