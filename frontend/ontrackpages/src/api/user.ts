import axios from "axios";


const LOGIN_URL = '/api/auth/login';

const REGISTER_URL = '/api/auth/register';

export const api = axios.create({
	baseURL: "http://localhost:5000",
});

export const createLoginSession = async (data: { email: string, password: string }) => {
	return await api.post(LOGIN_URL,
		JSON.stringify({
			...data
		}), 
		{
			headers: {
				'content-type': 'application/json'
		},
	});
};

export const createRegisterSession = async (data: { name: string, email: string, password: string }) => {
	return await api.post(REGISTER_URL,
		JSON.stringify({
			...data
		}), 
		{
			headers: {
				'content-type': 'application/json'
		},
	});
};