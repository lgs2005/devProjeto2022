import axios from "axios";


const mainApi = axios.create({
	baseURL: "http://localhost:5000",
	headers: {
		'content-type': 'application/json',
	}
})

export default mainApi;
