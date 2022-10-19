import React from 'react';
import ReactDOM from 'react-dom/client';

import { CssBaseline, GlobalStyles } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';

import { theme } from './theme/theming';

import { AuthController } from './controllers/globals';
import Router from './Router';


const appRoot = document.getElementById('react-app-root')!;

ReactDOM.createRoot(appRoot).render(
	<React.StrictMode>
		<ThemeProvider theme={theme}>
			<CssBaseline />
			<GlobalStyles styles={{ fontFamily: '"Roboto", sans-serif' }} />
			<AuthController>
				<Router />
			</AuthController>
		</ThemeProvider>
	</React.StrictMode>
);