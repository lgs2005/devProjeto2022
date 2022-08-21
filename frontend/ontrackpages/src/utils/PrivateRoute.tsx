import { useContext } from "react";
import { Navigate } from "react-router-dom";

import { AuthContext } from "../Contexts/AuthContextProvider";


export default function PrivateRoute({ children } : {children: JSX.Element}) {
	
	const { isAuthenticated } = useContext(AuthContext);

	if (!isAuthenticated) {
		return (
			<>
				<Navigate to='/login' />
			</>
		)
	}
	return children;
}