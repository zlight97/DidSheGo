// place files you want to import through the `$lib` alias in this folder.
import { goto } from "$app/navigation"
import { sendLogout } from "$lib/api"
export const logout = async () => {
    let auth = localStorage.getItem('token');
    if(auth)
    {
        const sessionUser = await sendLogout(auth).catch((error) => {
            console.log(error);
            return null;
        })
        localStorage.removeItem('token')
    }
    goto('/login')
}