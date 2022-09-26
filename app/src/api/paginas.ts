import { fetch2 } from "./api";
import { Pagina } from "./tipos";

function apiCriarPagina(nome: string) {
	return fetch2<Pagina>(
		'/api/pagina/criar',
		'POST',
		{ nome },
	);
}

function apiListarPaginas() {
	return fetch2<Pagina[]>(
		'/api/pagina/listar',
		'GET',
	);
}

function apiGetConteudo(id: number) {
	return fetch2<null>(
		'/api/conteudo/' + id.toString(),
		'GET',
	)
}

export { apiListarPaginas }