import TextField from '@mui/material/TextField';
import React from 'react';


type Props = {
	label: string,
	type: string,
	helperText: string,
	error: boolean,
	handleChange: React.ChangeEventHandler<HTMLInputElement>
};

export default function FormTextField({
	label,
	type,
	helperText,
	error,
	handleChange
}: Props) {

	return (
		<TextField
			variant='outlined'
			label={label}
			margin='normal'
			sx={{
				width: '100%'
			}}
			type={type}
			error={error}
			helperText={helperText}
			onChange={handleChange} />
	)
}