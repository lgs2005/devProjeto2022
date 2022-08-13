import styled from "styled-components"
import { useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";

import axios from "axios";

import Button from '@mui/material/Button';
import CheckBox from "@mui/material/Checkbox";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";


export default function Login() {

	interface InterfaceFormData {
		email: string,
		password: string
	};

	const [showPassword, setShowPassword] = useState(false);

	const [fields, setFields] = useState<InterfaceFormData>({
		email: "",
		password: "",
	});

	const onSubmit: SubmitHandler<InterfaceFormData> = async (formData) => {
		const response = await axios.post("http://localhost:5000/api/login", JSON.stringify({
			email: "email@gmail.com",
			senha: "senha",
			nome: "nome",
			registro: true,
		}), {
			headers: {
				'content-type': 'application/json'
			}
		})
			.then((response) => {
				console.log(response);
			})
			.catch((error) => {
				console.log(error);
			});
	};

	const { register, formState: { errors }, handleSubmit } = useForm<InterfaceFormData>();

	return (
		<Main>
			<Header>
				<h1>Welcome to <br />OnTrack Pages</h1>
			</Header>

			<SliderButtonGroup>
				<div style={{ display: 'grid' }}>
					<SliderButton data-slider-index="1">Login</SliderButton>
				</div>

				<div style={{ display: 'grid' }}>
					<SliderButton data-slider-index="2">Registrar</SliderButton>
				</div>
			</SliderButtonGroup>

			<form>
				<Grid
					container
					display="flex"
					flexDirection="column"
					flexWrap="wrap"
					minWidth="25vw">
					<Grid
						item
						xs={12}>
						<TextField
							variant="outlined"
							label="Email"
							margin="normal"
							sx={{
								width: "100%"
							}}

							id="login-email"
							type="email"

							{...register("email", { required: true })}
							aria-invalid={errors.email ? true : false}
							error={errors.email ? true : false}
							helperText={errors.email ? 'Preencha o campo' : ''}

							onChange={(e: React.ChangeEvent<HTMLInputElement>) => { setFields({ ...fields, email: e.target.value }) }} />

						<TextField
							variant="outlined"
							label="Senha"
							margin="normal"
							sx={{
								width: "100%"
							}}

							id="login-senha"
							type={showPassword? "text" : "password"}

							{...register("password", { required: true })}
							aria-invalid={errors.password ? true : false}
							error={errors.password ? true : false}
							helperText={errors.password ? 'Preencha o campo' : ''}

							onChange={(e: React.ChangeEvent<HTMLInputElement>) => { setFields({ ...fields, password: e.target.value }) }} />

						<Grid
							item
							display="flex"
							justifyContent="flex-end">
							<Typography
								margin="auto 0">Mostrar senha</Typography>
							<CheckBox size="small" name="password-show" onChange={() => setShowPassword(!showPassword)} />
						</Grid>

						<Grid
							container
							justifyContent="center"
							direction="row"
							alignItems="center"
							marginTop="2em">
							<Button
								type="submit"
								variant="outlined"
								sx={{
									minWidth: 180,
									borderRadius: 50
								}}>
								ENTRAR</Button>
						</Grid>
					</Grid>
				</Grid>
			</form>
		</Main>
	)
}


const Main = styled.div`
	display: flex;
	align-content: center;

	flex-direction: column;
	flex-wrap: wrap;
	height: 100vh;

	margin-top: 14vh;
`;

const Header = styled.div`
	text-align: center;
	margin-bottom: 2em;
`;

const SliderButton = styled.button`
	background-color: transparent;
	text-decoration: none;
	text-align: center;
	border: 0;
	flex-grow: 1;
	height: 34px;
	min-width: 10vh;

	cursor: pointer;
`;

const SliderButtonGroup = styled.div`
	display: flex;
	flex-direction: row;
	justify-content: space-around;
	
	margin-bottom: 2em;
`;