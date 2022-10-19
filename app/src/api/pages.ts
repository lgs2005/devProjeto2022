import { fetchAt } from "./api";
import { Page } from "./types";


export function apiCreatePage(dados: { name: string, folder: number }) {
	return fetchAt<Page>(
		'/api/pagina/criar',
		'POST',
		dados,
	);
}

export function apiListPages() {
	return fetchAt<Page[]>(
		'/api/pagina/listar',
		'GET',
	);
}

export function apiGetContent(id: number) {
	return fetchAt<string>(
		'/api/conteudo/' + id.toString(),
		'GET',
	)
}

export function apiPutContent(id: number, content: string) {
	return fetchAt<null>(
		'/api/conteudo/' + id.toString(),
		'PUT',
		{ content },
	)
}