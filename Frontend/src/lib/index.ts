// place files you want to import through the `$lib` alias in this folder.
import { goto } from "$app/navigation"
import { sendLogout } from "$lib/api"

export interface ActionEntry{
    actionid: number,
    name: string,
    time: number,
    deleted: boolean
}

export interface Login{
    success: boolean,
    token: string
}

export interface PetData{
    id: number,
    name: string,
    pos: number,
    time: number
}

// export interface NumberDataTuple extends Array<string|PetData>{0:string; 1:PetData}
export type NumberDataTuple = [string, Array<PetData>]
export interface PetInfo{
    [key: number]: NumberDataTuple
}

export const logout = async () => {
    let auth = localStorage.getItem('token');
    // localStorage.removeItem('email')
    // localStorage.removeItem('password')
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

export function updateToken(token: string)
{
    let curAuth = localStorage.getItem('token')
    if(token===curAuth)
        return curAuth;
    localStorage.setItem('token',token)
    return token;
}