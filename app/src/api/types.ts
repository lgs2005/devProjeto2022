export type User = {
	id: number,
	name: string,
	email: string,
}

export type Page = {
	id: number,
	id_author: number,
	name: string,
	favorite: boolean,
	creation_date: string,
	delete_date?: string,
}

export type Result<T, E> = { ok: true, value: T } | { ok: false, error: E };

