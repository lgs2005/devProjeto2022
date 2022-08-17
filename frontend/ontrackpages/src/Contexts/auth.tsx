import { createContext } from "react";


interface InterfaceAuthContext {
	isAuthenticated: boolean
	user: { email: string, password: string }
	registerUser: ({name, email, password} : {name: string, email: string, password: string}) => any
	loginUser: ({email, password} : {email: string, password: string}) => any,
	logoutUser: object
}

export const AuthContext = createContext<InterfaceAuthContext>({} as InterfaceAuthContext);