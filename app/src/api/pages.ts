import { fetch2 } from "./api";
import { Page } from "./types";


export function apiCreatePage(dados: { name: string, folder: number }) {
	return fetch2<Page>(
		'/api/pagina/criar',
		'POST',
		dados,
	);
}

export function apiListPages() {
	return fetch2<Page[]>(
		'/api/pagina/listar',
		'GET',
	);
}

export function apiGetContent(id: number) {
	return fetch2<string>(
		'/api/conteudo/' + id.toString(),
		'GET',
	)
}

export function apiPutContent(id: number, content: string) {
	return fetch2<null>(
		'/api/conteudo/' + id.toString(),
		'PUT',
		{ content },
	)
}