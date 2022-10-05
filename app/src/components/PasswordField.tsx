import { useState } from "react";

import { Checkbox, InputAdornment, TextField, TextFieldProps } from "@mui/material";

type PasswordFieldProps = Omit<TextFieldProps, 'type'|'InputProps'>

export default function PasswordField(props: PasswordFieldProps) {
	const [visible, setVisible] = useState(false);

	return <TextField
		{...props}
		type={ visible ? 'text' : 'password' }
		InputProps={{
			endAdornment: (
				<InputAdornment position='end'>
					{/* TODO: fazer isso ser um ícone. */}
					<Checkbox
						onChange={(_, checked) => setVisible(checked)}
					/>
				</InputAdornment>
			)
		}}
	/>
}