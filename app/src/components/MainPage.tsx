import { useEffect, useState } from "react";

import { fetchAt } from "../api/api";
import Sidebar from "./Sidebar";


export default function MainPage() {

    const [idPage, setIdPage] = useState<number | null>(null);
    const [content, setContent] = useState<string | null>(null);

    useEffect(() => {

        fetchAt<{markdown: { title: string, content: string }}>(
            '/api/conteudo/' + idPage,
            'GET',
        )
        .then(content => {
            setContent(content.markdown.title);
            console.log(content)
        });

    }, [idPage]);

    return <>
        <Sidebar onPageSelected={(id) => setIdPage(id)}>
            {content}
        </Sidebar>

        <div>
            {content}
        </div>
    </>
}