import { API_FULL_URL } from '$lib/constants';

export const userSignIn = async (email: string, password: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/submitlogin`, {
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

export const getPetInfo = async (auth: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/getpets`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8',
            "Access-Control-Allow-Headers": "x-requested-with",
            'Access-Token':auth
		}
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