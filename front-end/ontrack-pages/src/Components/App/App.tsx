import Login from '../Login/Login'
import { createGlobalStyle } from 'styled-components'

export default function App() {
	return (
		<>
			<GlobalStyle />
			<Login />
		</>
	)
}

const GlobalStyle = createGlobalStyle`
	* {
		margin: 0;
		padding: 0;
		font-family: "Roboto", sans-serif;
	}
`;