import { Request2 } from "./request2";

const base = new Request2('http://localhost:5000/api')

type Result<T, E> = { ok: true, value: T } | { ok: false, error: E };

type LoginError = 'baduser' | 'badpassword';
type RegisterError = 'bademail';
export type User = {
	name: string,
	email: string,
};

export namespace api {
	export function login(data: {email: string, password: string}) {
		let req = base.with(r => r
			.path('/auth/login')
			.json(data)
		);
	
		return req.fetch<Result<User, LoginError>>('POST');
	}
	
	export function register(data: {name: string, email: string, password: string}) {
		let req = base.with(r => r
			.path('/auth/register')
			.json(data)
		);
	
		return req.fetch<Result<User, RegisterError>>('POST');
	}
}