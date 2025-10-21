import {useAuth} from "../hooks/useAuth.ts";
import {useEffect, useState} from "react";
import api from "../api/api.ts";
import * as React from "react";

type VaultItem = { id: string; name: string; username?: string };

export default function Vault() {
    const [items, setItems] = useState<VaultItem[]>([]);
    const [newItem, setNewItem] = useState({ name: "", username: "", secret: "" });
    const { logout } = useAuth();

    const fetchItems = async () => {
        const { data } = await api.get("/passwords");
        setItems(data);
    }

    const addItem = async (e: React.FormEvent) => {
        e.preventDefault();
        await api.post("/passwords", newItem);
        setNewItem({ name: "", username: "", secret: "" });
        fetchItems();
    };

    useEffect(() => {
        fetchItems();
    }, []);

    return (
        <div className="vault-container" data-test-selector="vault_container">
            <h2 data-test-selector="vault_label">Your Vault</h2>
            <button data-test-selector="logout" onClick={logout}>Logout</button>

            <form onSubmit={addItem}>
                <input
                    data-test-selector="vault_name_input"
                    placeholder="Name"
                    value={newItem.name}
                    onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
                />
                <input
                    data-test-selector="vault_username_input"
                    placeholder="Username"
                    value={newItem.username}
                    onChange={(e) => setNewItem({ ...newItem, username: e.target.value })}
                />
                <input
                    data-test-selector="vault_password_input"
                    placeholder="Password/Secret"
                    value={newItem.secret}
                    onChange={(e) => setNewItem({ ...newItem, secret: e.target.value })}
                />
                <button data-test-selector="addNewPassword" type="submit">Add New Password</button>
            </form>

            <ul data-test-selector="storedPasswordList">
                {items.map((item) => (
                    <li key={item.id}>
                        <strong>{item.name}</strong> - {item.username}
                    </li>
                ))}
            </ul>
        </div>
    );
}