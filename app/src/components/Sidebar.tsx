import { PropsWithChildren, useCallback, useContext, useEffect, useState } from "react";

import { Grid, List, ListItemButton, ListItemIcon, ListItemText, Collapse, ListItem } from "@mui/material";

import LockIcon from '@mui/icons-material/Lock';
import NoteIcon from '@mui/icons-material/Note';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import FavoriteIcon from '@mui/icons-material/Favorite';
import { AuthControllerContext } from "../controllers/globals";
import { apiListarPaginas, Pagina } from "../api/auth";
import { fetch2 } from "../api/api";


const enum PagesList {
	Private,
	Favorite,
	Public,
	None
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

export default function Sidebar(props: PropsWithChildren<{ onPageSelected: (id: number) => void }>) {

	const [openPageList, setOpenPageList] = useState(PagesList.None);
	const [paginas, setPaginas] = useState<Pagina[]>([]);

	useEffect(() => {
        apiListarPaginas().then(
            paginas => {
                setPaginas(paginas);
            },

            err => {
                console.log(err)
            }
        );
    }, []);

	function criarListaPaginas(paginas: Pagina[]) {
		return paginas.map(p =>
			<ListItemButton
				onClick={() => props.onPageSelected(p.id)}
			>
				{p.nome}
			</ListItemButton>
		);
	}

	function listaPaginas(lista: PagesList) {
		if (lista == PagesList.Public) {
			return criarListaPaginas(paginas.filter(p => !p.favorito))
		} else if (lista == PagesList.Favorite) {
			criarListaPaginas(paginas.filter(p => p.favorito))
		} else {
			return <></>;
		}
	}

	
	return <>
		<button
			onClick={() => {
				fetch2<null>(
					'/api/criar-pagina',
					'POST',
					{
						nome: 'Sem título',
					}
				);
			}}
		>
			Criar Paginas
		</button>

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
									onClick={() => {
										if (pageContent.setEnum == openPageList) {
											setOpenPageList(PagesList.None)
										}
										else {
											setOpenPageList(pageContent.setEnum)
										}
									}}>
									<ListItemIcon>
										{pageContent.icon}
									</ListItemIcon>
									<ListItemText primary={pageContent.text.toUpperCase()} />

									{openPageList === pageContent.setEnum ? <ExpandLess /> : <ExpandMore />}
								</ListItemButton>

								<Collapse in={openPageList === pageContent.setEnum} unmountOnExit>
									<List>
										{ listaPaginas(pageContent.setEnum) }
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
				<h1>{props.children}</h1>
			</Grid>
		</Grid>
	</>
}