import { useContext, useEffect, useState } from "react";

import { Backdrop, CircularProgress } from "@mui/material";

import { AuthControllerContext } from "./controllers/AuthController";
import AuthPage from "./components/AuthPage";
import Sidebar from "./components/Sidebar";
import { api } from "./api/api";

export default function Main() {
	const userController = useContext(AuthControllerContext);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		api.getUser()
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