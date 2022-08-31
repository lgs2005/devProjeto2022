import { Alert, Backdrop, BackdropProps, Button, ButtonProps, CircularProgress, Collapse, Stack, TextField, TextFieldProps, Typography } from "@mui/material";
import { useContext, useState } from "react";
import { api } from "../api/api";
import { AuthControllerContext } from "../controllers/AuthController";
import useFormData from "../lib/useFormData";
import PasswordField from "./PasswordField";

const textFieldStyle: TextFieldProps = {
	variant: 'outlined',
	margin: 'normal',
	sx: {
		width: '100%',
	}
};

const submitButtonStyle: ButtonProps = {
	variant: 'outlined',
	sx: {
		minWidth: 230,
		minHeight: 50,
		borderRadius: 50,
		my: 3,
	},
};

function SFormBackdrop(props: BackdropProps) {
	return <Backdrop sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }} {...props}>
		<CircularProgress />
		<Typography
			variant="h4"
			sx={{ mx: 2 }}>
			Aguarde...
		</Typography>
	</Backdrop>
}

function SFormError(props: {onClose: () => void, message: string | null}) {
	return <Collapse
		in={props.message != null}>
		<Alert
			severity="error"
			onClose={props.onClose}>
			{props.message}
		</Alert>
	</Collapse>
}

function errorProps(error: string | null, setError: (err: null) => void): Partial<TextFieldProps> {
	return {
		error: error != null,
		helperText: error,
		onChange: () => setError(null),
	};
}

type LoginFormData = {
	email: string,
	password: string,
}

export function LoginForm() {
	const userController = useContext(AuthControllerContext)
	const [data,, onFieldChange] = useFormData<LoginFormData>({
		email: '',
		password: '',
	});
	
	const [processing, setProcessing] = useState(false);
	const [serverError, setServerError] = useState<string | null>(null);
	const [emailError, setEmailError] = useState<string | null>(null);
	const [passwordError, setPasswordError] = useState<string | null>(null);
	
	const onSubmitForm: React.FormEventHandler<HTMLFormElement> = async (e) => {
		e.preventDefault();
		setProcessing(true);

		await api.login(data).then(
			res => {
				if (res.ok) {
					userController.setValue(res.value);
				} else if (res.error === 'no-such-user') {
					setEmailError('Este usuário não existe.');
				} else if (res.error === 'wrong-password') {
					setPasswordError('Senha incorreta.');
				} else {
					setServerError('Ocorreu um erro desconhecido, tente novamente mais tarde.');
				}
			},

			err => {
				setServerError('Não foi possível fazer login, tente novamente mais tarde.');
			}
		);

		setProcessing(false);
	}

	return <>
		<SFormBackdrop open={processing} />
		<form onSubmit={onSubmitForm} onChange={onFieldChange}>
			<Stack
				alignItems='center'>

				<TextField
					name='email'
					type='email'
					value={data.email}
					autoComplete='username'
					required
					
					label='Email'
					{...errorProps(emailError, setEmailError)}
					{...textFieldStyle}
					/>

				<PasswordField
					name='password'
					value={data.password}
					autoComplete='current-password'
					required
					
					label='Senha'
					{...errorProps(passwordError, setPasswordError)}
					{...textFieldStyle}
					/>

				<Button
					type='submit'
					{...submitButtonStyle}>
					ENTRAR
				</Button>

			</Stack>
		</form>
		<SFormError message={serverError} onClose={() => setServerError(null)} />
	</>
}

type RegisterFormData = {
	name: string,
	email: string,
	password: string,
}

export function RegisterForm() {
	const userController = useContext(AuthControllerContext);
	const [data,, onFieldChange] = useFormData<RegisterFormData>({
		name: '',
		email: '',
		password: '',
	});

	const [processing, setProcessing] = useState(false);
	const [serverError, setServerError] = useState<string | null>(null);
	const [emailError, setEmailError] = useState<string | null>(null);
	
	const onSubmitForm: React.FormEventHandler = async (e) => {
		e.preventDefault();
		setProcessing(true);

		await api.register(data).then(
			res => {
				if (res.ok) {
					userController.setValue(res.value);
				} else if (res.error === 'already-exists') {
					setEmailError('Um usuário com este email já existe.')
				} else {
					setServerError('Ocorreu um erro desconhecido, tente novamente mais tarde.');
				}
			},

			err => {
				setServerError('Não foi possível fazer login, tente novamente mais tarde.');
			}
		);

		setProcessing(false);
	}

	return <>
		<SFormBackdrop open={processing} />
		<form onSubmit={onSubmitForm} onChange={onFieldChange}>
			<Stack
				alignItems='center'>

				<TextField
					name='name'
					type='text'
					value={data.name}
					required

					label='Nome'
					{...textFieldStyle}
				/>

				<TextField
					name='email'
					type='email'
					value={data.email}
					autoComplete='username'
					required

					label='Email'
					{...errorProps(emailError, setEmailError)}
					{...textFieldStyle}
				/>

				<PasswordField
					name='password'
					value={data.password}
					autoComplete='current-password'
					required

					label='Senha'
					{...textFieldStyle}
				/>

				<Button
					type='submit'
					{...submitButtonStyle}>
					REGISTRAR
				</Button>

			</Stack>
		</form>
		<SFormError message={serverError} onClose={() => setServerError(null)} />
	</>
}