import { Request2 } from "./request2";

// CORS diferencia entre localhost e 127.0.0.1
// se usar o ip errado não serão enviados os cookies de autenticação
// solução: usar outra coisa
// TODO: ^^^^^^
const base = new Request2('http://127.0.0.1:5000')
.with(r => r
	.setCredentials('include')
	.setMode('cors')
);

type Result<T, E> = { ok: true, value: T } | { ok: false, error: E };

type LoginError = 'no-such-user' | 'wrong-password';
type RegisterError = 'already-exists';

export type User = {
	name: string,
	email: string,
};

export namespace api {
	export function login(data: {email: string, password: string}) {
		let req = base.with(r => r
			.path('/api/auth/login')
			.json(data)
		);
	
		return req.fetch<Result<User, LoginError>>('POST');
	}
	
	export function register(data: {name: string, email: string, password: string}) {
		let req = base.with(r => r
			.path('/api/auth/register')
			.json(data)
		);
	
		return req.fetch<Result<User, RegisterError>>('POST');
	}

	export function getUser() {
		let req = base.with(r => r
			.path('/api/auth/user')
			.setCredentials('include')
		);

		return req.fetch<User, User | null>('GET', {
			ok: user => user,
			401: () => null,
		});
	}
}