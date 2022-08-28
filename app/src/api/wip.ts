interface RequestOptions {
	url: URL | string
	body?: string
	contentType?: string
}

class Request2 {
	opts: RequestOptions
	constructor(opts: RequestOptions) {
		this.opts = opts;
	}

	private fetch(method: string) {
		return fetch(this.opts.url, {
			method: method,
			body: this.opts.body,
			headers: {
				'Content-Type': this.opts.contentType!,
			},
		});
	}

	private copy(opts: Partial<RequestOptions>) {
		return new Request2(Object.assign({...this.opts}, opts));
	}

	path(path: string) {
		return this.copy({
			url: new URL(path, this.opts.url)
		})
	}

	json(data: any) {
		return this.copy({
			body: JSON.stringify(data),
			contentType: 'application/json',
		})
	}

	post() {
		return this.fetch('POST');
	}
}

const api = new Request2({ url: 'localhost:5000' })

export function login2(username: string, password: string) {
	return api.path('/auth/login').json({ username, password }).post();
}

export function register2(username: string, password: string, email: string) {
	return api.path('/auth/register').json({ username, password, email }).post()
}