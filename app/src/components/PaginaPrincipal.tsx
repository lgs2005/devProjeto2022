import { useEffect, useState } from "react";
import { fetch2 } from "../api/api";
import Sidebar from "./Sidebar";

export default function PaginaPrincipal() {

    const [idPagina, setIdPagina] = useState<number | null>(null);
    const [conteudo, setConteudo] = useState<string | null>(null);

    useEffect(() => {

        fetch2<{markdown: { titulo: string, conteudo: string }}>(
            '/api/conteudo/' + idPagina,
            'GET',
        )
        .then(conteudo => {
            setConteudo(conteudo.markdown.titulo);
            console.log(conteudo)
        });

    }, [idPagina]);

    return <>
        <Sidebar onPageSelected={(id) => setIdPagina(id)}>
            {conteudo}
        </Sidebar>

        <div>
            {conteudo}
        </div>
    </>
}