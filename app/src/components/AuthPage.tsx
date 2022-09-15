import { Alert, Backdrop, CircularProgress, Collapse, Container, Tab, Tabs, Typography } from "@mui/material";
import { useState, useContext } from "react"
import { FormSubmitHandler } from "../lib/useFormSchema";
import { LoginForm, LoginFormData, RegisterForm, RegisterFormData } from "./AuthForms";
import SwipeViewsContainer from "./SwipeViewsContainer";
import { AuthControllerContext } from "../controllers/globals";
import { apiLogin, apiRegister } from "../api/auth";


export default function AuthPage() {
	const [currentTab, setCurrentTab] = useState(0);
	const [isFetching, setIsFetching] = useState(false);
	const [globalError, setGlobalError] = useState<string | null>(null);
	const userController = useContext(AuthControllerContext);

	const submitRegisterForm: FormSubmitHandler<RegisterFormData> = async (data, setError) => {
		setIsFetching(true);
		await apiRegister(data).then(
			res => {
				if (res.ok) {
					userController.setValue(res.value);
				} else if (res.error === 'already-exists') {
					setError('email', 'Um usuário com este email já existe');
				} else {
					setGlobalError('Ocorreu um erro desconhecido, tente novamente mais tarde.');
				}
			},

			_ => {
				setGlobalError('Não foi possível fazer login, tente novamente mais tarde.');
			}
		);
		setIsFetching(false);
	}

	const submitLoginForm: FormSubmitHandler<LoginFormData> = async (data, setError) => {
		setIsFetching(true);
		await apiLogin(data).then(
			res => {
				if (res.ok) {
					userController.setValue(res.value);
				} else if (res.error === 'no-such-user') {
					setError('email', 'Este usuário não existe.');
				} else if (res.error === 'wrong-password') {
					setError('password', 'Senha incorreta.');
				} else {
					setGlobalError('Ocorreu um erro desconhecido, tente novamente mais tarde.');
				}
			},

			_ => {
				setGlobalError('Não foi possível fazer login, tente novamente mais tarde.');
			}
		);
		setIsFetching(false);
	}

	return <>
		<Container maxWidth='sm'>

			<Typography
				variant='h3'
				textAlign='center'
				marginTop='1em'>
				Welcome to <br/>OnTrack Pages
			</Typography>

			<Tabs
				value={currentTab}
				onChange={(_, v) => setCurrentTab(v)}
				variant='fullWidth'
				sx={{my: 2}}>
				<Tab label='Login' value={0} />
				<Tab label='Cadastrar' value={1} />
			</Tabs>

			<SwipeViewsContainer currentIndex={currentTab}>
				<LoginForm onSubmit={submitLoginForm} />
				<RegisterForm onSubmit={submitRegisterForm} />
			</SwipeViewsContainer>

			<Collapse in={globalError != null}>
				<Alert
					severity='error'
					onClose={ () => setGlobalError(null) }>
					{globalError}
				</Alert>
			</Collapse>

			<Backdrop open={isFetching}>
				<CircularProgress />
				<Typography
					variant='h4'
					sx={{ mx: 2 }}>
					Aguarde...
				</Typography>
			</Backdrop>
		</Container>
	</>
}