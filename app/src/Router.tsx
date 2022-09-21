import { useContext, useEffect, useState } from "react";

import { Backdrop, CircularProgress } from "@mui/material";

import { AuthControllerContext } from "./controllers/globals";
import AuthPage from "./components/AuthPage";
import Sidebar from "./components/Sidebar";
import { apiGetUser } from "./api/auth";

export default function Router() {
	const userController = useContext(AuthControllerContext);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		apiGetUser()
			.catch(() => null)
			.then(userController.setValue)
			.then(() => setLoading(false))
	// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	if (loading) {
		return <Backdrop open>
			<CircularProgress />
		</Backdrop>
	}

	if (userController.value == null) {
		return <AuthPage />
	}

	return <>
		<Sidebar />
	</>;
}