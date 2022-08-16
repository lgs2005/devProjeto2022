import { useState } from 'react';

import Grid from '@mui/material/Grid';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import ToggleButton from '@mui/material/ToggleButton';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import LoginForm from '../../Components/LoginForm';
import RegisterForm from '../../Components/RegisterForm';


export default function Login() {

	const [currentForm, setCurrentForm] = useState('login');

	return (
		<>
			<Typography
				textAlign='center'
				variant='h3'
				marginTop='1em'>
				Welcome to <br />OnTrack Pages</Typography>

			<ToggleButtonGroup
				color='primary'
				size='small'
				sx={{
					display: 'flex',
					justifyContent: 'center',
					margin: '2em 0 2em 0'
				}}>

				<ToggleButton
					value='login'
					sx={{
						flexGrow: 1,
						maxWidth: 140
					}}
					onClick={(() => { setCurrentForm('login') })}>
					LOGIN
				</ToggleButton>

				<ToggleButton
					value='cadastrar'
					sx={{
						flexGrow: 1,
						maxWidth: 140
					}}
					onClick={(() => { setCurrentForm('register') })}>
					CADASTRAR
				</ToggleButton>
			</ToggleButtonGroup>
			
			<Grid
				container
				justifyContent='center'>
				<Grid
					display='grid'
					gridTemplateColumns='minmax(120px, 480px)'
					sx={{
						transform: currentForm === 'register' ? 'translate(-100%)' : 'translateX(0)',
						transition: 'transform ease 300ms'
					}}>
					<Grid
						gridArea={1/1}
						sx={{
							opacity: currentForm === 'login' ? 1 : 0,
							transition: 'opacity ease 300ms'
						}}>
						<LoginForm />
					</Grid>
					<Grid
						gridArea={1/1}
						sx={{
							opacity: currentForm === 'login' ? 0 : 1,
							transition: 'opacity ease 300ms'
						}}>
						<RegisterForm />
					</Grid>
				</Grid>
			</Grid>
		</>
	)
}