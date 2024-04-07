import { API_BASE_URL } from '$lib/constants';

export const userSignIn = async (email: string, password: string) => {
	let error = null;

	const res = await fetch(`http://${API_BASE_URL}/submitlogin`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8',
            "Access-Control-Allow-Headers": "x-requested-with"
		},
		body: JSON.stringify({
			email: email,
			password: password
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);

			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};