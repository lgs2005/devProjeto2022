import { useContext } from "react";
import AuthPage from "./components/AuthPage";
import { AuthControllerContext } from "./controllers/AuthController";

export default function Main() {
	const userController = useContext(AuthControllerContext);

	if (userController.value == null) {
		return <AuthPage />
	}

	return <>
		Yoooooo
	</>;
}