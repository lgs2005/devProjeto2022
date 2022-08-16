import TextField from '@mui/material/TextField';
import React from 'react';
import { UseFormRegisterReturn } from 'react-hook-form';

export default function FormTextField({ label, type, useFormRegisterReturn, ariaInvalid, error, helperText, handleChange } : 
	{ label: string, type: string, useFormRegisterReturn: UseFormRegisterReturn, ariaInvalid: boolean, error: boolean, helperText: string, handleChange: React.ChangeEventHandler<HTMLInputElement> }) {
	
	return (
		<TextField
			variant='outlined'
			label={label}
			margin='normal'
			sx={{
				width: '100%'
			}}
			type={type}
			{...useFormRegisterReturn}
			aria-invalid={ariaInvalid}
			error={error}
			helperText={helperText}
			onChange={handleChange} />
	)
}