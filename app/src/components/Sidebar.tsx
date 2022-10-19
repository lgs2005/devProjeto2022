import { PropsWithChildren, useState, useEffect } from "react";

import { Typography, Drawer, Box, useMediaQuery, useTheme } from "@mui/material";

const drawerWidth = 240;

export default function Sidebar(props: PropsWithChildren<{ onPageSelected: (id: number) => void }>)  {
	
	const [ open, setOpen ] = useState(true);

	const shouldCollapse = useMediaQuery('(max-width: 1280px)')

	useEffect(() => {
		shouldCollapse? setOpen(false) : setOpen(true);
	}, [shouldCollapse])
	
	return <>
		<Drawer variant={'persistent'} open={open}>
			<Box width={drawerWidth}>
				<Typography>
					oi
				</Typography>
			</Box>
		</Drawer>

		<Box component='main' height='100vh' width={`calc(100% - ${drawerWidth}px)`}>
			hrlo
		</Box>

	</>
}