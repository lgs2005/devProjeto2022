import { useState } from "react";

import { Grid, List, ListItemButton, ListItemIcon, ListItemText, Collapse } from "@mui/material";

import LockIcon from '@mui/icons-material/Lock';
import NoteIcon from '@mui/icons-material/Note';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import FavoriteIcon from '@mui/icons-material/Favorite';


const enum PagesList {
	Private,
	Favorite,
	Public
};

const FAKE_DATA = [
	'Page1',
	'Page2',
	'Pagec',
]

const PageListItem = [
	{
		icon: <FavoriteIcon/>,
		text: 'favoritas',
		setEnum: PagesList.Favorite
	},
	{
		icon: <LockIcon/>,
		text: 'privadas',
		setEnum: PagesList.Private
	},
	{
		icon: <NoteIcon/>,
		text: 'públicas',
		setEnum: PagesList.Public
	}
]

export default function Sidebar() {

	const [openPageList, setOpenPageList] = useState(PagesList.Public);

	return (
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

				<List
					sx={{
						minWidth: '100%'
					}}>
	
					{PageListItem.map((pageContent: { icon: JSX.Element, text: string, setEnum: PagesList }) => {
						return (
							<>
								<ListItemButton
									onClick={() => setOpenPageList(pageContent.setEnum)}>
									<ListItemIcon>
										{pageContent.icon}
									</ListItemIcon>
									<ListItemText primary={pageContent.text.toUpperCase()} />

									{openPageList === pageContent.setEnum ? <ExpandLess /> : <ExpandMore />}
								</ListItemButton>

								<Collapse in={openPageList === pageContent.setEnum} unmountOnExit>
									<List>
										{FAKE_DATA.map((name) => <ListItemButton>{name}</ListItemButton>)}
									</List>
								</Collapse>
							</>
						)
					})}
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