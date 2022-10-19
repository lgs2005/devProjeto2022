import { fetch2 } from "./api";
import { User } from "./types";


export enum LoginError {
	NoSuchUser,
	WrongPassword,
}

export function apiLogin(data: { email: string, password: string }) {
	return fetch2<User, User | LoginError>(
		'/api/auth/login',
		'POST',
		data,
		{
			ok: (user) => user,
			404: () => LoginError.NoSuchUser,
			409: () => LoginError.WrongPassword,
		}
	);
}


export enum RegisterError {
	EmailInUse
}
	
export function apiRegister(data: { name: string, email: string, password: string }) {
	return fetch2<User, User | RegisterError>(
		'/api/auth/register',
		'POST',
		data,
		{
			ok: (user) => user,
			409: () => RegisterError.EmailInUse,
		}
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


export enum AlterError {
	EmailInUse
}

export function apiAlterUser(dados: {
	password: string,
	new: {
		password: string,
		name: string,
		email: string,
	}
}) {
	return fetch2<User, User | AlterError>(
		'/api/auth/alter',
		'PATCH',
		dados,
		{
			ok: (user) => user,
			409: () => AlterError.EmailInUse,
		}
	)
}
