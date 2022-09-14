import { Button, ButtonProps, Stack, TextField, TextFieldProps } from "@mui/material";
import useFormSchema, { FormSubmitHandler } from "../lib/useFormSchema";
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

export type LoginFormData = {
	email: string,
	password: string,
}

export function LoginForm(props: { onSubmit: FormSubmitHandler<LoginFormData> }) {
	const [data,, errors,, onFieldChange, wrapSubmitHandler] = useFormSchema<LoginFormData>({
		email: '',
		password: '',
	});

	return <form onSubmit={wrapSubmitHandler(props.onSubmit)} onChange={onFieldChange}>
		<Stack
			alignItems='center'>

			<TextField
				name='email'
				type='email'
				value={data.email}
				autoComplete='username'
				required
				
				label='Email'
				error={errors.email != null}
				helperText={errors.email}
				{...textFieldStyle}
				/>

			<PasswordField
				name='password'
				value={data.password}
				autoComplete='current-password'
				required
				
				label='Senha'
				error={errors.password != null}
				helperText={errors.password}
				{...textFieldStyle}
				/>

			<Button
				type='submit'
				{...submitButtonStyle}>
				ENTRAR
			</Button>

		</Stack>
	</form>
}

export type RegisterFormData = {
	name: string,
	email: string,
	password: string,
}

export function RegisterForm(props: { onSubmit: FormSubmitHandler<RegisterFormData> }) {
	const [data,, errors,, onFieldChange, wrapSubmitHandler] = useFormSchema<RegisterFormData>({
		name: '',
		email: '',
		password: '',
	});

	return <form onSubmit={wrapSubmitHandler(props.onSubmit)} onChange={onFieldChange}>
		<Stack
			alignItems='center'>

			<TextField
				label='Nome'
				name='name'
				type='text'
				value={data.name}
				required

				{...textFieldStyle}
			/>

			<TextField
				label='Email'
				name='email'
				type='email'
				value={data.email}
				autoComplete='username'
				required

				error={errors.email != null}
				helperText={errors.email}
				{...textFieldStyle}
			/>

			<PasswordField
				label='Senha'
				name='password'
				value={data.password}
				autoComplete='current-password'
				required

				{...textFieldStyle}
			/>

			<Button
				type='submit'
				{...submitButtonStyle}>
				REGISTRAR
			</Button>

		</Stack>
	</form>
}