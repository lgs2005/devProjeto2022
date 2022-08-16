import Button from '@mui/material/Button';

export default function ButtonPill({ buttonType, buttonText } : {buttonType: 'button'|'reset'|'submit', buttonText: string }) {
	return (
		<Button
			type={buttonType}
			variant='outlined'
			sx={{
				minWidth: 180,
				borderRadius: 50
			}}>
			{buttonText.toUpperCase()}</Button>
	)
}