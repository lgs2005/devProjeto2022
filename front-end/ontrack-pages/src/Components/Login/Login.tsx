import styled from 'styled-components'

export default function Login() {
	return (
		<div>
			<Main>
				<Header>
					<h1>Welcome to <br />OnTrack Pages</h1>
				</Header>
				
				<Form>
					<InputGroup>
						<label htmlFor="login-email">
							Email
						</label>
	
						<Input id="login-email" type="email" />
					</InputGroup>
					
					<InputGroup>
						<label htmlFor="login-senha">
							Senha
						</label>
						<Input id="login-senha" type="password" />
					</InputGroup>

					<ButtonGroup>
						<Button type="submit">ENTRAR</Button>
					</ButtonGroup>
				</Form>
			</Main>
		</div>
	)
}

const Main = styled.div`
	display: flex;
	justify-content: center;
	align-content: center;

	flex-direction: column;
	flex-wrap: wrap;
	height: 100vh;
`;

const Form = styled.form`
	display: flex;
	flex-direction: column;

	min-width: 26vw;
`;

const InputGroup = styled.div`
	display: flex;
	flex-direction: column;
	margin-bottom: 12px;
`;

const Input = styled.input`
	min-height: 28px;
	border-radius: 6px;

	border: 1px solid gray;
`

const Header = styled.div`
	text-align: center;
`;

const Button = styled.button`
	text-align: center;
	margin-top: 12px;
	padding: 6px 48px;

	border-radius: 500px;
`;

const ButtonGroup = styled.div`
	display: flex;
	justify-content: center;
`;