import { AxiosResponse } from "axios";
import { createContext } from "react";


interface InterfaceAuthContext {
	isAuthenticated: boolean
	user: { email: string, password: string }
	register: ({name, email, password} : {name: string, email: string, password: string}) => AxiosResponse<any, any> | any
	login: ({email, password} : {email: string, password: string}) => AxiosResponse<any, any> | any,
	logout: object
}

export const AuthContext = createContext<InterfaceAuthContext>({
	isAuthenticated: false,
	user: { email: '', password: '' },
	register: ({  }) => {console.log('default')},
	login: ({ name: '', email: '', password: '' }) => {console.log('default')},
	logout: {}
});