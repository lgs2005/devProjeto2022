import { User } from "./api_types";
import fetch2b from "./fetch2b";

export enum LoginError {
    WrongPassword,
    DoesntExist,
}

export enum RegisterError {
    EmailConflict,
}

export function api_loginUser(email: string, password: string) {
    return fetch2b<User | LoginError>('/api/auth/login', 'POST', { email, password }, {
        409: () => LoginError.WrongPassword,
        404: () => LoginError.DoesntExist,
    })
}

export function api_registerUser(name: string, email: string, password: string) {
    return fetch2b<User | RegisterError>('/api/auth/register', 'POST', { name, email, password }, {
        403: () => RegisterError.EmailConflict,
    })
}

export function api_currentUser() {
    return fetch2b<User | null>('/api/auth/user', 'GET', undefined, { 401: () => null });
}