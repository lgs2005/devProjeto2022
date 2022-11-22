import { useState, useContext } from "react"

import { Alert, Backdrop, CircularProgress, Collapse, Container, Tab, Tabs, Typography } from "@mui/material";

import { LoginForm, LoginFormData, RegisterForm, RegisterFormData } from "./AuthForms";
import { AuthControllerContext } from "../controllers/globals";
import { apiLogin, apiRegister, LoginError, RegisterError } from "../api/auth";
import { FormSubmitHandler } from "../lib/useFormSchema";
import SwipeViewsContainer from "./SwipeViewsContainer";
import { resourceUsage } from "process";


export default function AuthPage() {
	const [currentTab, setCurrentTab] = useState(0);
	const [isFetching, setIsFetching] = useState(false);
	const [globalError, setGlobalError] = useState<string | null>(null);

	const userController = useContext(AuthControllerContext);

	const submitRegisterForm: FormSubmitHandler<RegisterFormData> = async (data, setError) => {
		setIsFetching(true);
		await apiRegister(data).then(
			res => {
				if (res == RegisterError.EmailInUse) {
					setError('email', 'Um usuário com este email já existe');
				} else {
					userController.setValue(res);
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
				if (res == LoginError.NoSuchUser) {
					setError('email', 'Este usuário não existe.');
				}
				else if (res == LoginError.WrongPassword) {
					setError('password', 'Senha incorreta.');
				}
				else {
					userController.setValue(res);
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

			<Collapse in={globalError != null}>
				<Alert
					sx={{
						my: 2
					}}
					severity='error'
					onClose={ () => setGlobalError(null) }>
					{globalError}
				</Alert>
			</Collapse>

			<SwipeViewsContainer currentIndex={currentTab}>
				<LoginForm onSubmit={submitLoginForm} />
				<RegisterForm onSubmit={submitRegisterForm} />
			</SwipeViewsContainer>


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