import { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';

import CheckBox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

import mainApi from '../api/user';

import ButtonPill from './ButtonPill';
import FormTextField from './FormTextField';


export default function LoginForm() {

	interface InterfaceFields {
		email: string,
		password: string
	};

	interface InterfaceFieldsErrors {
		emailHintError: string,
		passwordHintError: string
	};

	const [showPassword, setShowPassword] = useState(false);

	const [fields, setFields] = useState<InterfaceFields>({
		email: '',
		password: '',
	});

	const [fieldsError, setFieldsErrors] = useState<InterfaceFieldsErrors>({
		emailHintError: '',
		passwordHintError: ''
	});

	const onSubmit: SubmitHandler<InterfaceFields> = async (formData) => {
		const response = await mainApi.post('/api/login', JSON.stringify({
			email: formData.email,
			senha: formData.password
		}))
			.then((response) => {
				if (response.data.sucesso) {
					console.log('Redirecionar para a página principal da aplicação')
				} else {
					response.data.errtarget === 'email' ?
						setFieldsErrors({ ...fieldsError, emailHintError: response.data.erro }) :
						setFieldsErrors({ ...fieldsError, passwordHintError: response.data.erro })
				}

			})
			.catch((error) => {
				console.log(error);
			});
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
						fieldsError.emailHintError ? true : false}
				helperText={
					fieldsError.emailHintError ?
						fieldsError.emailHintError :
						errors.email ? 'Preencha o campo' : ''}
				handleChange={(e: React.ChangeEvent<HTMLInputElement>) => { setFields({ ...fields, email: e.target.value }) }} />

			<FormTextField
				label='Senha'
				type={showPassword ? 'text' : 'password'}
				useFormRegisterReturn={register('password', { required: true })}
				ariaInvalid={errors.password ? true : false}
				error={
					errors.password ? true : false ||
						fieldsError.passwordHintError ? true : false}
				helperText={
					fieldsError.passwordHintError ?
						fieldsError.passwordHintError :
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