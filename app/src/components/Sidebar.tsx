import { PropsWithChildren, useState, useEffect } from "react";

import { Typography, Drawer, Box, useMediaQuery, Grid, List, ListItemButton } from "@mui/material";
import { apiListPages } from "../api/pages";
import { Page } from "../api/types";

const drawerWidth = 240;

export default function Sidebar(props: PropsWithChildren<{ onPageSelected: (id: number) => void }>)  {
	
	const [ open, setOpen ] = useState(true);
	const [paginas, setPaginas] = useState<Page[]>([]);

	useEffect(() => {
        apiListPages().then(
            paginas => {
				console.log(paginas)
                setPaginas(paginas);
            },

            err => {
                console.log(err)
            }
        );
    }, []);

	const shouldCollapse = useMediaQuery('(max-width: 1280px)')

	useEffect(() => {
		shouldCollapse? setOpen(false) : setOpen(true);
	}, [shouldCollapse])
	
	return <>
		<Grid
			container
			spacing={2}>
			<Grid
				item
				alignContent='center'
				flexDirection='column'
				sm={4}
				md={3}
				lg={2}
				sx={{
					maxWidth: '230px',
					minHeight: '102vh',
					maxHeight: '100%',
					backgroundColor: '#ECECEC',
					boxShadow: '0 0 1em #808080'
				}}>

				<List>
					{ paginas.map(p => <>
						<ListItemButton
							onClick={() => props.onPageSelected(p.id)}
						>
							{p.name}
						</ListItemButton>
					</> )}
				</List>
			</Grid>

			<Grid
				item
				xs={8}>
				<h1>{props.children}</h1>
			</Grid>
		</Grid>

		{/* <Drawer variant={'persistent'} open={open}>
			<Box width={drawerWidth}>
				<Typography>
					
				</Typography>
			</Box>
		</Drawer>

		<Box component='main' height='100vh' width={`calc(100% - ${drawerWidth}px)`}>
			hrlo
		</Box> */}

	</>
}