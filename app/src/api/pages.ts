import { fetchAt } from "./api";
import { Page } from "./types";


function apiCreatePage(nome: string) {
	return fetchAt<Page>(
		'/api/pagina/criar',
		'POST',
		{ nome },
	);
}

function apiListPages() {
	return fetchAt<Page[]>(
		'/api/pagina/listar',
		'GET',
	);
}

function apiGetContent(id: number) {
	return fetchAt<null>(
		'/api/conteudo/' + id.toString(),
		'GET',
	)
}

export { apiListPages, apiCreatePage, apiGetContent }