import { Backdrop, CircularProgress } from "@mui/material";
import { useState, useEffect } from "react"
import { User } from "./api/api_types";
import { api_currentUser } from "./api/authentication";
import AuthPage from "./components/AuthPage";
import MainPage from "./components/MainPage";
import { UserContext } from "./global_context"

export default function Router() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api_currentUser()
            .catch(() => null)
            .then(setUser)
            .then(() => setLoading(false));
    }, []);

    if (loading) {
        return <Backdrop open>
            <CircularProgress />
        </Backdrop>
    }

    if (user == null) {
        return <AuthPage onLoginFinish={setUser} />
    }

    return <UserContext.Provider value={user}>
        <MainPage />
    </UserContext.Provider>
}