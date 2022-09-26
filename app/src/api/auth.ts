import { fetch2 } from "./api";
import { Result, Usuario } from "./tipos";

type LoginError = 'no-such-user' | 'wrong-password';
type RegisterError = 'already-exists';

function apiLogin(data: { email: string, password: string }) {
	return fetch2<Result<Usuario, LoginError>>(
		'/api/auth/login',
		'POST',
		data
	);
}

function apiRegister(data: { name: string, email: string, password: string }) {
	return fetch2<Result<Usuario, RegisterError>>(
		'/api/auth/register',
		'POST',
		data
	);
}

function apiGetUser() {
	return fetch2<Usuario, Usuario | null>(
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
	return fetch2<Usuario, Usuario | null>(
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