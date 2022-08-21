import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AuthProvider } from '../Contexts/AuthContextProvider';

import AppPage from '../Pages/App/AppPage';
import LoginPage from '../Pages/Login/LoginPage';
import NOT_FOUND from '../Pages/Handlers/404';

import PrivateRoute from "../utils/PrivateRoute";


export default function AppRouter() {
	return (
		<BrowserRouter>
			<AuthProvider>
				<Routes>
					<Route path="/" element={
						<PrivateRoute>
							<AppPage />
						</PrivateRoute>
					} />
					<Route path="/login" element={<LoginPage />} />
					<Route path="*" element={<NOT_FOUND />} />
				</Routes>
			</AuthProvider>
		</BrowserRouter>
	)
}