import axios from "axios";

export default axios.create({
	baseURL: "http://localhost:5000/api/login",
	headers: {
		'Content-Type': 'application/json',
	}
})