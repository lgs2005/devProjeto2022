import { fetch2, Result } from "./api";

type LoginError = 'no-such-user' | 'wrong-password';
type RegisterError = 'already-exists';

export type User = {
	name: string,
	email: string,
};

export type Pagina = {
	id: number,
	nome: string,
	favorito: boolean
;}

export function apiLogin(data: { email: string, password: string }) {
	return fetch2<Result<User, LoginError>>(
		'/api/auth/login',
		'POST',
		data
	);
}

export function apiRegister(data: { name: string, email: string, password: string }) {
	return fetch2<Result<User, RegisterError>>(
		'/api/auth/register',
		'POST',
		data
	);
}

export function apiGetUser() {
	return fetch2<User, User | null>(
		'/api/auth/user',
		'GET',
		undefined,
		{
			ok: user => user,
			401: () => null,
		}
	);
}

export function apiListarPaginas() {
	return fetch2<Pagina[]>(
		'/api/listar-paginas',
		'GET',
	);
}