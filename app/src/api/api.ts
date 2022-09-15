const BASE_URL = 'http://127.0.0.1:5000';
const TOKEN_UPDATE_HEADER = 'X-OTP-Update-Bearer-Token';
const TOKEN_STORAGE_KEY = 'otp-bread-token';

export type Result<T, E> = { ok: true, value: T } | { ok: false, error: E };

export type FetchHandlers<T, R> = {
	[code: number]: (res: Response) => R,
	ok: (data: T) => R,
}

export async function fetch2<T, R=T>(
	path: string,
	method: 'GET' | 'POST' | 'PUT' | 'PATCH',
	data?: any,
	handlers?: FetchHandlers<T, R>
) {
	let url = BASE_URL + path;
	let options: RequestInit = {};
	let token = sessionStorage.getItem(TOKEN_STORAGE_KEY);

	options.method = method;
	options.headers = {};

	if (method !== 'GET' && data !== undefined) {
		options.headers['Content-Type'] = 'application/json';
		options.body = JSON.stringify(data);
	}

	if (token) {
		options.headers['Authorization'] = 'Bearer ' + token;
	}

	let res = await fetch(url, options);
	let new_token = res.headers.get(TOKEN_UPDATE_HEADER);

	if (new_token) {
		sessionStorage.setItem(TOKEN_STORAGE_KEY, new_token);
	}

	if (res.ok) {
		let data = await res.json() as T;

		if (handlers) {
			return handlers.ok(data);
		} else {
			return data;
		}
	} else if (handlers && res.status in handlers) {
		return handlers[res.status](res);
	} else {
		throw Error(`Server responded with ${res.status}`)
	}
}