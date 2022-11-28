import { Checkbox, InputAdornment, TextField, TextFieldProps } from "@mui/material";
import { useState } from "react";

export type PasswordFieldProps = Omit<TextFieldProps, 'type' | 'InputProps'>

export default function PasswordField(props: PasswordFieldProps) {
    const [visible, setVisible] = useState(false);

    return <TextField
        {...props}
        type={ visible ? 'text' : 'password' }
        InputProps={{
            endAdornment: (
                <InputAdornment position='end'>
                    {/* TODO: ícone */}
                    <Checkbox 
                        onChange={(_, checked) => setVisible(checked)}
                    />
                </InputAdornment>
            )
        }}
    />
}
