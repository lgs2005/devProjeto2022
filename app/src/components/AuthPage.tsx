import { Alert, Backdrop, CircularProgress, Collapse, Container, Tab, Tabs, Typography } from "@mui/material";
import { useCallback, useState } from "react";
import { User } from "../api/api_types";
import { api_loginUser, api_registerUser, LoginError, RegisterError } from "../api/authentication";
import { FormSubmitHandler } from "../useFormSchema";
import { LoginForm, LoginFormData, RegisterForm, RegisterFormData } from "./AuthForms";
import SwipeTabsContainer from "./SwipeTabsContainer";

export default function AuthPage(props: { onLoginFinish: (user: User) => void }) {
    const [tab, setTab] = useState(0);
    const [fetching, setFetching] = useState(false);
    const [globalError, setGlobalError] = useState<string | null>(null);

    const submitLoginForm: FormSubmitHandler<LoginFormData> = useCallback(async (data, setError) => {
        setFetching(true);
        await api_loginUser(data.email, data.password).then(
            (res) => {
                if (res == LoginError.DoesntExist)
                    setError('email', 'Este usuário não existe.')
                else if (res == LoginError.WrongPassword)
                    setError('password', 'Senha incorreta.')
                else
                    props.onLoginFinish(res)
            },

            _ => {
                setGlobalError('Não conseguimos realizar seu login. Tente novamente mais tarde.');
            }
        )
        setFetching(false);
    }, []);

    const submitRegisterForm: FormSubmitHandler<RegisterFormData> = useCallback(async (data, setError) => {
        setFetching(true);
        await api_registerUser(data.name, data.email, data.password).then(
            (res) => {
                if (res == RegisterError.EmailConflict)
                    setError('email', 'Este usuário já existe.')
                else
                    props.onLoginFinish(res);
            },

            _ => {
                setGlobalError('Não conseguimos realizar seu cadastro. Tente novamente mais tarde.');
            }
        )
        setFetching(false);
    }, []);

    return <Container maxWidth='sm'>
        <Typography
            variant='h3'
            textAlign='center'
            marginTop='1em'
        >
            Welcome to <br /> OnTrack Pages
        </Typography>

        <Tabs
            value={tab}
            onChange={(_, newTab) => setTab(newTab)}
            variant='fullWidth'
            sx={{ my: 2 }}
        >
            <Tab label='Login' value={0} />
            <Tab label='Cadastrar' value={1} />
        </Tabs>

        <Collapse in={globalError != null}>
            <Alert
                sx={{
                    my: 2
                }}
                severity='error'
                onClose={() => setGlobalError(null)}
            >
                {globalError}
            </Alert>
        </Collapse>

        <SwipeTabsContainer currentIndex={tab}>
            <LoginForm onSubmit={submitLoginForm} />
            <RegisterForm onSubmit={submitRegisterForm} />
        </SwipeTabsContainer>

        <Backdrop open={fetching}>
            <CircularProgress />
            <Typography
                variant='h4'
                sx={{ mx: 2 }}
            >
                Aguarde...
            </Typography>
        </Backdrop>
    </Container>
}