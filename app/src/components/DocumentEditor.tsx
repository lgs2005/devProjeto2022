import { CircularProgress } from "@mui/material";
import { useEffect, useState } from "react";

export default function DocumentEditor({ documentID }: { documentID: number }) {
    const [loadingContent, setLoadingContent] = useState(false)

    useEffect(() => {

    }, [documentID])

    if (loadingContent) {
        return <CircularProgress />
    }

    return <>
        Content
    </>
}