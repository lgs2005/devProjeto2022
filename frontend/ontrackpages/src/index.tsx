import React from 'react';
import ReactDOM from 'react-dom/client';

import { createGlobalStyle } from 'styled-components';

import AppRouter from './Routes/AppRouter';


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
		<AppRouter />
		<GlobalStyle />
	</React.StrictMode>
);

