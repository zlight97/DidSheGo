// place files you want to import through the `$lib` alias in this folder.
import { goto } from "$app/navigation"
export function logout()
{
    localStorage.removeItem('token')
    goto('/login')
}