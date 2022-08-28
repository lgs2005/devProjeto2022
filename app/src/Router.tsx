import { useContext } from "react";
import AuthPage from "./components/AuthPage";
import { AuthContext } from "./controllers/AuthController";

export default function Router() {
	const user = useContext(AuthContext);

	if (user.value == null) {
		return <AuthPage />
	}

	return <>

	</>;
}