import { Backdrop, CircularProgress } from "@mui/material";
import { useContext, useEffect, useState } from "react";
import { api } from "./api/api";
import AuthPage from "./components/AuthPage";
import { AuthControllerContext } from "./controllers/AuthController";

export default function Router() {
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
		Yoooooo
	</>;
}