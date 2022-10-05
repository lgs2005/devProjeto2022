import { fetchAt } from "./api";
import { Result, User } from "./types";


type LoginError = 'no-such-user' | 'wrong-password';
type RegisterError = 'already-exists';

function apiLogin(data: { email: string, password: string }) {
	return fetchAt<Result<User, LoginError>>(
		'/api/auth/login',
		'POST',
		data
	);
}

function apiRegister(data: { name: string, email: string, password: string }) {
	return fetchAt<Result<User, RegisterError>>(
		'/api/auth/register',
		'POST',
		data
	);
}

function apiGetUser() {
	return fetchAt<User, User | null>(
		'/api/auth/user',
		'GET',
		undefined,
		{
			ok: user => user,
			401: () => null,
		}
	);
}

function apiMudarSenha(dados: { old_password: string, new_password: string }) {
	return fetchAt<User, User | null>(
		'/api/auth/alterar-senha',
		'POST',
		dados,
		{
			ok: user => user,
			401: () => null,
		}
	);
}

export { apiLogin, apiRegister, apiGetUser, apiMudarSenha }