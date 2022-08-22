import React from 'react'; 

import Button from '@mui/material/Button';


type TypeButtonPill = {
	type: 'button' | 'reset' | 'submit' | undefined,
	text: string | JSX.Element,
	handleOnClick: () => void
};

export default function ButtonPill({ type, text, handleOnClick } : TypeButtonPill) {
	return (
		<Button
			type={type}
			variant='outlined'
			sx={{
				minWidth: 180,
				borderRadius: 50
			}}
			onClick={handleOnClick}>
			{text}</Button>
	)
}