type User = {
	id: number,
	name: string,
	email: string,
}

type Page = {
	id: number,
	id_author: number,
	name: string,
	favorite: boolean,
	creation_date: string,
	delete_date?: string,
}

type Result<T, E> = { ok: true, value: T } | { ok: false, error: E };

export type { User, Page, Result }