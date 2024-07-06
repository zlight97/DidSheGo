import { API_FULL_URL } from '$lib/constants';

export const createNewPet = async (petName: string, auth: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/newpet`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
		},
		body: JSON.stringify({
			auth: auth,
			petname: petName
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
}

export const createNewAction = async (actionName: string, petid: number, auth: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/newaction`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
		},
		body: JSON.stringify({
			auth: auth,
			petid: petid,
			action: actionName
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
}


export const deleteOrRestoreAction = async (actionid: number, auth: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/updateaction`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
		},
		body: JSON.stringify({
			auth: auth,
			actionid: actionid
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
}

export const getPetList = async (auth: string, petid: number) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/getallactions`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
		},
		body: JSON.stringify({
			auth: auth,
			petid: petid
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

export const userSignIn = async (email: string, password: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/submitlogin`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
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


export const createAccount = async (email: string, password: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/createaccount`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
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

export const sendLogout = async (auth: string) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/logout`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
		},
		body: JSON.stringify({
			auth: auth
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

export const submitTime = async (auth: string, actionId: number, time:EpochTimeStamp) => {
	let error = null;

	const res = await fetch(`${API_FULL_URL}/submitTime`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=UTF-8'
		},
		body: JSON.stringify({
			auth: auth,
			id: actionId,
			time: time
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