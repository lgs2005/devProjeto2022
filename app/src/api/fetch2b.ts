const BASE_URL = 'http://127.0.0.1:5000'

export default async function fetch2b<T>(
    path: string,
    method: 'GET' | 'POST' | 'PUT' | 'PATCH',
    data?: any,
    handlers?: { [status: number]: (res: Response) => T },
) {
    let url = new URL(path, BASE_URL);
    let options: RequestInit = {};
    let token = sessionStorage.getItem('otp-bread-token');

    options.method = method;
    options.headers = {};

    if (token !== null) {
        options.headers['Authorization'] = 'Bearer ' + token;
    }

    if (data !== undefined) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(data);
    }

    let response = await fetch(url, options);
    let new_token = response.headers.get('X-OTP-Update-Bearer');

    if (new_token !== null) {
        sessionStorage.setItem('otp-bread-token', new_token);
    }

    if ((handlers !== undefined) && (response.status in handlers)) {
        return handlers[response.status](response);
    }
    else if (response.ok) {
        return await response.json() as T;
    }
    else {
        throw Error('Unhandled response ' + response.status);
    }
}