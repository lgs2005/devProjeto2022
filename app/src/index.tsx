import React from 'react';
import ReactDOM from 'react-dom/client';
import Router from './Router';
import { AuthController } from './controllers/AuthController';
import { CssBaseline, GlobalStyles } from '@mui/material';

const appRoot = document.getElementById('react-app-root')!;

ReactDOM.createRoot(appRoot).render(
	<React.StrictMode>
		<CssBaseline />
		<GlobalStyles styles={{ fontFamily: '"Roboto", sans-serif' }} />
		<AuthController>
			<Router />
		</AuthController>
	</React.StrictMode>
);