import { ExpandLess, ExpandMore } from "@mui/icons-material";
import { CircularProgress, Collapse, Grid, List, ListItemButton, ListItemText } from "@mui/material";
import { PropsWithChildren, useEffect, useState } from "react";
import { Folder } from "../api/api_types";
import { api_doclistFull } from "../api/documents";
import DocumentEditor from "./DocumentEditor";

export default function MainPage(props: PropsWithChildren<{}>) {
    const [documentList, setDocumentList] = useState<Folder[]>([]);
    const [loadingDocuments, setLoadingDocuments] = useState(true);
    const [currentDocument, setCurrentDocument] = useState(0);

    useEffect(() => {
        api_doclistFull()
            .then(setDocumentList)
            .then(() => setLoadingDocuments(false))
            .catch(() => alert('Couldnt load document list'))
    }, []);

    return <>
        <Grid container spacing={2}>
            <Grid item
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
                    boxShadow: '0 0 1em #808080',
                }}
            >
                {
                    loadingDocuments
                        ? <CircularProgress />
                        : <DocumentList list={documentList} onSelect={setCurrentDocument} />
                }
            </Grid>

            <Grid item xs={8}>
                <DocumentEditor
                    documentID={currentDocument}
                />
                {/*
                <button
                    onClick={() => {
                        api_doclistFull().then(data => alert(JSON.stringify(data)))
                    }}
                >
                    Click me
                </button>
                */}
            </Grid>
        </Grid>
    </>
}

function DocumentList(props: { list: Folder[], onSelect: (docid: number) => void }) {
    const [openLists, setOpenLists] = useState<{ [name: string]: boolean }>({});

    return (
        <List sx={{ minWidth: '100%' }}>
            {props.list.map((folder, index) => <div key={index}>
                <ListItemButton
                    onClick={() => {
                        setOpenLists({ ...openLists, [folder.name]: !openLists[folder.name] })
                    }}
                >
                    <ListItemText primary={folder.name} />
                    {openLists[folder.name] ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>

                <Collapse in={openLists[folder.name]}>
                    {folder.pages.map((page, index) => <List key={index}>
                        <ListItemButton
                            onClick={ () => { props.onSelect(page.id) } }
                        >
                            {page.name}
                        </ListItemButton>
                    </List>)}
                </Collapse>
            </div>)}
        </List>
    )
}