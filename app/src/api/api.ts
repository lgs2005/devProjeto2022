import { Request2 } from "./request2";

const base = new Request2('http://localhost:5000')

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
		);

		return req.fetch<User, User | null>('GET', {
			ok: user => user,
			401: () => null,
		});
	}
}