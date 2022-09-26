type Usuario = {
	id: number,
	nome: string,
	email: string,
}

type Pagina = {
	id: number,
	id_autor: number,
	nome: string,
	favorito: boolean,
	data_criacao: string,
	data_excluir?: string,
}

type Result<T, E> = { ok: true, value: T } | { ok: false, error: E };

export type { Usuario, Pagina, Result }