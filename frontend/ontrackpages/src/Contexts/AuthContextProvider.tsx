import React, { createContext, useState } from "react";

import { NavigateFunction, useNavigate } from 'react-router-dom';


interface InterfaceUser {
	email: string,
	password: string
}

interface InterfaceAuthContext {
	isAuthenticated: boolean,
	user: { email: string, password: string },
	setUser: React.Dispatch<React.SetStateAction<InterfaceUser>>,
	navigate: NavigateFunction,
	logoutUser: object
}

export const AuthContext = createContext<InterfaceAuthContext>({} as InterfaceAuthContext);

export function AuthProvider(props: React.PropsWithChildren) {

	const [user, setUser] = useState<InterfaceUser>({
		email: '',
		password: ''
	});

	const navigate = useNavigate();

	function logoutUser() {
		setUser({ email: '', password: '' });
		navigate('/login')
	};

	return (
		<AuthContext.Provider
			value={{
				isAuthenticated: !!user.email && !!user.password,
				user,
				setUser,
				navigate,
				logoutUser
			}}>
			{props.children}
		</AuthContext.Provider>
	)
}