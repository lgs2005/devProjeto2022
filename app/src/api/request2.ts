export class RequestOptions {
	url: URL
	body?: string
	contentType?: string

	constructor(url: URL) {
		this.url = url
	}

	clone() {
		return Object.assign(
			Object.create(
				Object.getPrototypeOf(this)),
			this
		);
	}

	path(path: string) {
		this.url = new URL(path, this.url);
		return this;
	}

	json(data: any) {
		this.body = JSON.stringify(data);
		this.contentType = 'application/json';
		return this;
	}
}

type FetchHandlers<T, R> = {
	[code: number]: (res: Response) => R,
	ok: (data: T) => R,
}

export class Request2 {
	opts: RequestOptions

	constructor(opts: RequestOptions)
	constructor(url: string | URL)
	constructor(optsOrURL: RequestOptions | string | URL) {
		if (optsOrURL instanceof RequestOptions) {
			this.opts = optsOrURL;
		} else {
			this.opts = new RequestOptions(new URL(optsOrURL))
		};
	}

	async fetch<T, R=T>(method: string, handlers?: FetchHandlers<T, R>) {
		let res = await fetch(this.opts.url, {
			method: method,
			body: this.opts.body,
			headers: {
				'Content-Type': this.opts.contentType ?? 'text/plain'
			},
		})

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

	with(change: (req: RequestOptions) => RequestOptions) {
		return new Request2(change(this.opts.clone()));
	}
}