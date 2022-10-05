import { PropsWithChildren } from "react";

import { Grid, Typography } from "@mui/material";

export default function Sidebar(props: PropsWithChildren<{ onPageSelected: (id: number) => void }>)  {
	return <>
		<Grid container spacing={0}>
			<Grid item xs={3} md={2}>
				<Typography color={primary.main}>
					oi
				</Typography>
			</Grid>

			<Grid item xs={8}>
				Dashboard
			</Grid>
		</Grid>
	</>
}