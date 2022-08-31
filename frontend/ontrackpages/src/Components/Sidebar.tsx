import { useState } from "react";

import { Grid, List, ListItemButton, ListItemIcon, ListItemText, useAutocomplete } from "@mui/material";

import LockIcon from '@mui/icons-material/Lock';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import FavoriteIcon from '@mui/icons-material/Favorite';


const enum PagesList {
	Private,
	Favorite,
	Public,
	None,
};

const FAKE_DATA = [
	'Page1',
	'Page2',
	'Pagec'
]

export default function Sidebar() {

	const [openPageList, setOpenPageList] = useState(PagesList.Public);

	return (
		<Grid container>
			<Grid
				container
				alignContent='center'
				flexDirection='column'
				xs={2}
				sx={{
					maxWidth: '230px',
					minHeight: '100vh',
					maxHeight: '100%',
					backgroundColor: '#ECECEC',
					boxShadow: '0 0 1em #808080'
				}}>
				
				<List>
					<ListItemButton
						onClick={() => setOpenPageList(PagesList.Favorite)}>
						<ListItemIcon>
							<FavoriteIcon />
						</ListItemIcon>
						<ListItemText primary="Páginas favoritas" />

						<List>
							{FAKE_DATA.map((item) => item)}
						</List>

						{openPageList === PagesList.Favorite ? <ExpandLess /> : <ExpandMore />}
					</ListItemButton>

					<ListItemButton
						onClick={() => setOpenPageList(PagesList.Private)}>
						<ListItemIcon>
							<LockIcon />
						</ListItemIcon>
						<ListItemText primary="Páginas privadas" />
						{openPageList === PagesList.Private ? <ExpandLess /> : <ExpandMore />}
					</ListItemButton>
					
					<ListItemButton
						onClick={() => setOpenPageList(PagesList.Public)}>
						<ListItemText primary="Páginas privadas" />
						{openPageList === PagesList.Public ? <ExpandLess /> : <ExpandMore />}
					</ListItemButton>

					
				</List>
			</Grid>

			<Grid
				item
				xs={8}>
				<h1>Dashboard</h1>
			</Grid>
		</Grid>
	)
}