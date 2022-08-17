import { useState } from "react";
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom";

import AppPage from '../Pages/App/AppPage';
import LoginPage from '../Pages/Login/LoginPage';
import _404 from '../Pages/Handlers/404';

import { AuthContext } from '../Contexts/auth';
import mainApi from "../api/user";


export default function AppRouter() {

	const [ user, setUser ] = useState({
		email: '',
		password: ''
	});

	const loginUser = (data: { email: string, password: string }) => {
		const response = mainApi.post('/api/auth/login', JSON.stringify({
			...data
		}))
			.then((response) => response)
			.catch((e) => e)
	};
	
	const registerUser = (data: { name: string, email: string, password: string }) => {
		const response = mainApi.post('/api/auth/register', JSON.stringify({
			...data
		}))
			.then((response) => response)
			.catch((e) => console.log(e))
	};

	function logout() {
		return
	};

	return (
		<BrowserRouter>
			<AuthContext.Provider value={{
					isAuthenticated: !!user,
					user,
					loginUser,
					registerUser,
					logoutUser: logout
				}}>
				<Routes>
					<Route path="/" element={<AppPage />} />
					<Route path="/login" element={<LoginPage />} />
					<Route path="*" element={<_404 />} />
				</Routes>
			</AuthContext.Provider>
		</BrowserRouter>
	)
}