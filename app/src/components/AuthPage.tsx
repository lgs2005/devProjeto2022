import { Container, Tab, Tabs, Typography } from "@mui/material";
import { useState } from "react"
import { LoginForm, RegisterForm } from "./AuthForms";
import SwipeViewsContainer from "./SwipeViewsContainer";

export default function AuthPage() {
	const [currentTab, setCurrentTab] = useState(0);

	return <>
		<Container maxWidth='sm'>

			<Typography
				variant='h3'
				textAlign='center'
				marginTop='1em'>
				Welcome to <br/>OnTrack Pages
			</Typography>

			<Tabs
				value={currentTab}
				onChange={(_, v) => setCurrentTab(v)}
				variant='fullWidth'
				sx={{my: 2}}>
				<Tab label='Login' value={0} />
				<Tab label='Cadastrar' value={1} />
			</Tabs>

			<SwipeViewsContainer currentIndex={currentTab}>
				<LoginForm />
				<RegisterForm />
			</SwipeViewsContainer>

		</Container>
	</>
}