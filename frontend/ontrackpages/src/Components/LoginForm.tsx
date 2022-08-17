import { useState, useContext } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

import CheckBox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

import { AuthContext } from '../Contexts/auth'; 

import ButtonPill from './ButtonPill';
import FormTextField from './FormTextField';


export default function LoginForm() {

	interface InterfaceFields {
		email: string,
		password: string
	};

	interface InterfaceFieldsErrors {
		emailErrorHint: string,
		passwordErrorHint: string
	};

	const navigate = useNavigate();
		
	const { isAuthenticated, loginUser } = useContext(AuthContext);

	const [showPassword, setShowPassword] = useState(false);

	const [fields, setFields] = useState<InterfaceFields>({
		email: '',
		password: '',
	});

	const [fieldsError, setFieldsErrors] = useState<InterfaceFieldsErrors>({
		emailErrorHint: '',
		passwordErrorHint: ''
	});

	const onSubmit: SubmitHandler<InterfaceFields> = async (formData) => {
		const response = loginUser({ ...formData });

		if (response.sucesso) {
			navigate('/', { replace: true })
		} else {
			response.data.errtarget === 'email' ?
				setFieldsErrors({ ...fieldsError, emailErrorHint: response.data.erro }) :
				setFieldsErrors({ ...fieldsError, passwordErrorHint: response.data.erro })
		}
	};

	const { register, formState: { errors }, handleSubmit } = useForm<InterfaceFields>();

	return (
		<form onSubmit={handleSubmit(onSubmit)}>
			<FormTextField
				label='Email'
				type='email'
				useFormRegisterReturn={register('email', { required: true })}
				ariaInvalid={errors.email ? true : false}
				error={
					errors.email ? true : false ||
						fieldsError.emailErrorHint ? true : false}
				helperText={
					fieldsError.emailErrorHint ?
						fieldsError.emailErrorHint :
						errors.email ? 'Preencha o campo' : ''}
				handleChange={(e: React.ChangeEvent<HTMLInputElement>) => { setFields({ ...fields, email: e.target.value }) }} />

			<FormTextField
				label='Senha'
				type={showPassword ? 'text' : 'password'}
				useFormRegisterReturn={register('password', { required: true })}
				ariaInvalid={errors.password ? true : false}
				error={
					errors.password ? true : false ||
						fieldsError.passwordErrorHint ? true : false}
				helperText={
					fieldsError.passwordErrorHint ?
						fieldsError.passwordErrorHint :
						errors.password ? 'Preencha o campo' : ''}
				handleChange={(e: React.ChangeEvent<HTMLInputElement>) => { setFields({ ...fields, password: e.target.value }) }} />

			<Grid
				container
				justifyContent='flex-end'>
				<Typography
					margin='auto 0'>
					Mostrar senha</Typography>
				<CheckBox
					size='small'
					name='password-show'
					onChange={() => setShowPassword(!showPassword)} />
			</Grid>

			<Grid
				container
				justifyContent='center'
				marginTop='1.2em'>
				<ButtonPill buttonText='entrar' buttonType='submit' />
			</Grid>
		</form>
	)
}