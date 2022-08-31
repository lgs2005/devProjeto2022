import { Button, ButtonProps, Stack, TextField, TextFieldProps } from "@mui/material";
import { api } from "../api/api";
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

type LoginFormData = {
	email: string,
	password: string,
}

type RegisterFormData = {
	name: string,
	email: string,
	password: string,
}

export function LoginForm() {
	const [data,, onFieldChange] = useFormData<LoginFormData>({
		email: '',
		password: '',
	});

	const onSubmitForm: React.FormEventHandler<HTMLFormElement> = (e) => {
		e.preventDefault();

		api.login(data).then(
			res => {

			},

			err => {

			}
		);
	}

	return <>
		<form onSubmit={onSubmitForm} onChange={onFieldChange}>
			<Stack
				alignItems='center'>

				<TextField
					label='Email'
					name='email'
					type='email'
					required
					value={data.email}
					autoComplete='username'
					{...textFieldStyle}
				/>
				<PasswordField
					label='Senha'
					name='password'
					required
					value={data.password}
					autoComplete='current-password'
					{...textFieldStyle}
				/>
				<Button
					type='submit'
					{...submitButtonStyle}>
					ENTRAR
				</Button>

			</Stack>
		</form>
	</>
}

export function RegisterForm() {
	const [data,, onFieldChange] = useFormData<RegisterFormData>({
		name: '',
		email: '',
		password: '',
	});

	const onSubmitForm: React.FormEventHandler = (e) => {
		e.preventDefault();

		api.register(data).then(
			res => {

			},

			err => {

			}
		);
	}

	return <>
		<form onSubmit={onSubmitForm} onChange={onFieldChange}>
			<Stack
				alignItems='center'>

				<TextField
					label='Nome'
					name='name'
					type='text'
					required
					value={data.name}
					{...textFieldStyle}
				/>
				<TextField
					label='Email'
					name='email'
					type='email'
					required
					value={data.email}
					autoComplete='username'
					{...textFieldStyle}
				/>
				<PasswordField
					label='Senha'
					name='password'
					required
					value={data.password}
					autoComplete='current-password'
					{...textFieldStyle}
				/>
				<Button
					type='submit'
					{...submitButtonStyle}>
					REGISTRAR
				</Button>

			</Stack>
		</form>
	</>
}