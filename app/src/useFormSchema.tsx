import React, { useState } from "react";

export type FormSubmitHandler<T extends object> = (
    data: T,
    setError: (field: keyof T, error: string) => void,
) => Promise<void>;

export default function useFormSchema<T extends object>(initialValue: T) {
    const [formData, setFormData] = useState(initialValue);
    const [formErrors, setFormErrors] = useState({} as T);

    function setFieldError(field: keyof T, error: string) {
        setFormErrors({
            ...formErrors,
            [field]: error,
        });
    }

    function setFieldData<F extends keyof T>(field: F, data: T[F]) {
        setFormData({
            ...formData,
            [field]: data,
        });
    }

    const onFieldChange: React.ChangeEventHandler<HTMLFormElement> = (e) => {
        if (!(e.target.name in formData)) {
            console.error(`Form schema entry with name ${e.target.name} does not exist.`);
        }
        else {
            setFormData({
                ...formData,
                [e.target.name]: e.target.value,
            });
            setFormErrors({
                ...formErrors,
                [e.target.name]: null,
            });
        }
    }

    function wrapSubmitHandler(handler: FormSubmitHandler<T>): React.FormEventHandler {
        return async (e) => {
            e.preventDefault();
            await handler(formData, setFieldError);
        };
    }

    return [formData, formErrors, setFieldData, setFieldError, onFieldChange, wrapSubmitHandler] as const;
}