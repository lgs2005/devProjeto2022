import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { createGlobalStyle } from 'styled-components';

import Login from './Routes/Login/LoginPage';
import App from './Routes/App/AppPage';

const GlobalStyle = createGlobalStyle`
	* {
		margin: 0;
		padding: 0;
		font-family: "Roboto", sans-serif;
	}
`;

const root = ReactDOM.createRoot(
	document.getElementById('root') as HTMLElement
);
root.render(
	<React.StrictMode>
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<App />} />
				<Route path="/login" element={<Login />} />
				<Route
					path="*"
					element={
						<main style={{textAlign: 'center'}}>
							<p>404</p>
						</main>
					}
				/>
			</Routes>
		</BrowserRouter>
		<GlobalStyle />
	</React.StrictMode>
);

