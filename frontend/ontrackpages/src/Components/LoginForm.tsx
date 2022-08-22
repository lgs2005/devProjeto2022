import React, { useState, useContext, useEffect } from 'react';

import CheckBox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Collapse from '@mui/material/Collapse';

import { AuthContext } from '../Contexts/AuthContextProvider';

import ButtonPill from './ButtonPill';
import FormTextField from './FormTextField';

import GenericErrorAlert from './GenericError';
import validateFormFields from '../utils/form_utils'
import { createLoginSession } from '../api/user';
import { CircularProgress } from '@mui/material';


export default function LoginForm() {

	interface InterfaceFields {
		email: string,
		password: string
	};

	const initialValues: InterfaceFields = {
		email: '',
		password: ''
	};

	const { setUser, navigate } = useContext(AuthContext);

	const [isLoading, setIsLoading] = useState(false);

	const [showPassword, setShowPassword] = useState(false);

	const [showGenericError, setShowGenericError] = useState(false);

	const [fields, setFields] = useState(initialValues);

	const [fieldsErrors, setFieldsErrors] = useState(initialValues);

	useEffect(() => (
		setFieldsErrors({ ...fieldsErrors, email: '' })
	), [fields.email])

	useEffect(() => (
		setFieldsErrors({ ...fieldsErrors, password: '' })
	), [fields.password])

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		const areFieldsFilled = validateFormFields(fields);

		if (areFieldsFilled) {
			await createLoginSession({ ...fields })
				.then((response) => {
					if (response.data.sucess) {
						setUser({ ...fields });
						navigate('/');
					} else {
						setFieldsErrors({
							...fieldsErrors,
							[response.data.err_target]: response.data.error
						})
					}
				})
				.catch((err) => setShowGenericError(true));
		} else {
			setFieldsErrors({
				email: !!fields.email ? '' : 'Preencha o campo',
				password: !!fields.password ? '' : 'Preencha o campo',
			})
		}
	};

	return (
		<form onSubmit={handleSubmit}>
			<Collapse
				in={!!showGenericError}
				sx={{
					paddingBottom: 2
				}}>
				<GenericErrorAlert severity='error' handleIconOnClickButton={() => setShowGenericError(false)} message='Sem conexão com o servidor.' />
			</Collapse>

			<FormTextField
				label='Email'
				type='email'
				error={!!fieldsErrors.email}
				helperText={fieldsErrors.email ?? ''}
				handleChange={(e: React.ChangeEvent<HTMLInputElement>) => { setFields({ ...fields, email: e.target.value }) }} />

			<FormTextField
				label='Senha'
				type={showPassword ? 'text' : 'password'}
				error={!!fieldsErrors.password}
				helperText={fieldsErrors.password ?? ''}
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
				<ButtonPill 
					text={isLoading? <CircularProgress /> : 'ENTRAR'} 
					type='submit' 
					handleOnClick={validateFormFields(fields)? setIsLoading(true) : setIsLoading(false)}/>
			</Grid>
		</form>
	)
}