import Button from '@mui/material/Button';


type TypeButtonPill = {
	type: 'button' | 'reset' | 'submit' | undefined,
	text: string | JSX.Element,
};

export default function ButtonPill({ type, text } : TypeButtonPill) {
	return (
		<Button
			type={type}
			variant='outlined'
			sx={{
				minWidth: 180,
				borderRadius: 50
			}}>
			{text}</Button>
	)
}