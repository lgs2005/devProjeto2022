import React from 'react';

import { Alert, AlertColor, IconButton } from '@mui/material';

import CloseIcon from '@mui/icons-material/Close';


type Props = {
	severity: AlertColor, 
	message: string,
	handleIconOnClickButton: React.MouseEventHandler<HTMLButtonElement>
};

export default function GenericErrorAlert({ message, severity, handleIconOnClickButton } : Props) {
	return (
	<Alert 
		severity={severity}
		action={
			<IconButton
				aria-label="close"
				color="inherit"
				size="small"
				onClick={handleIconOnClickButton}
			>
				<CloseIcon fontSize="inherit" />
			</IconButton>
			}>{message}</Alert>
	);
}