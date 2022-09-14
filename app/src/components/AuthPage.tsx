import { Container, Tab, Tabs, Typography } from "@mui/material";
import { useState } from "react"
import { FormSubmitHandler } from "../lib/useFormSchema";
import { LoginForm, RegisterForm, RegisterFormData } from "./AuthForms";
import SwipeViewsContainer from "./SwipeViewsContainer";
import { api } from "../api/api";


// const [processing, setProcessing] = useState(false);
// 	const [serverError, setServerError] = useState<string | null>(null);
// 	const [emailError, setEmailError] = useState<string | null>(null);
	
	const onSubmitForm: FormSubmitHandler<RegisterFormData> = async (data, setError) => {
		//setProcessing(true);

		await api.register(data).then(
			res => {
				if (res.ok) {
					// userController.setValue(res.value);
				} else if (res.error === 'already-exists') {
					setError('email', 'Um usuário com este email já existe');
				} else {
					//setServerError('Ocorreu um erro desconhecido, tente novamente mais tarde.');
				}
			},

			err => {
				//setServerError('Não foi possível fazer login, tente novamente mais tarde.');
			}
		);

		// setProcessing(false);
	}


export default function AuthPage() {
	const [currentTab, setCurrentTab] = useState(0);

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
				<LoginForm />
				<RegisterForm onSubmit={onSubmitForm} />
			</SwipeViewsContainer>

		</Container>
	</>
}