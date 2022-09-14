import React, { useState } from "react";

export default function useFormSchema<T>(initialValues: T) {
    const [formData, setFormData] = useState(initialValues);
    const [formErrors, setFormErrors] = useState({} as T);

    const onFieldChange: React.ChangeEventHandler<HTMLFormElement> = (e) => {
        if (e.target.name in formData) {            
			setFormData({
				...formData,
				[e.target.name]: e.target.value
			});

            setFormErrors({
                ...formErrors,
                [e.target.name]: null,
            });
		} else {
			console.error(`Form data entry with name ${e.target.name} does not exist.`);
		}
    };

    function setFieldError(field: keyof T, error: string) {
        setFormErrors({
            ...formErrors,
            [field]: error,
        });
    };

    function setFieldData<F extends keyof T>(field: F, data: T[F]) {
        setFormData({
            ...formData,
            [field]: data,
        });
    };

    function wrapSubmitHandler(handler: FormSubmitHandler<T>): React.FormEventHandler {
        return async (e) => {
            e.preventDefault();
            await handler(formData, setFieldError);
        }
    }

    return [formData, setFieldData, formErrors, setFieldError, onFieldChange, wrapSubmitHandler] as const;
}

export type FormSubmitHandler<T> = (data: T, setError: (field: keyof T, error: string) => void) => Promise<void>;

// type User = {
//     email: string,
//     senha: string,
// }

// const [data, setFieldData, errors, setFieldError, onFieldChange] = useFormSchema<User>({
//     email: 'lgs22264@gmail.com',
//     senha: '123',
// });

// setFieldData('email', 'ok')
// setFieldError('email', 'ok')