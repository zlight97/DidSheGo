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


export function shadeColor(color: string, percent: number) {

    var R = parseInt(color.substring(1,3),16);
    var G = parseInt(color.substring(3,5),16);
    var B = parseInt(color.substring(5,7),16);

    R = R * (100 + percent) / 100;
    G = G * (100 + percent) / 100;
    B = B * (100 + percent) / 100;

    R = (R<255)?R:255;  
    G = (G<255)?G:255;  
    B = (B<255)?B:255;  

    R = Math.round(R)
    G = Math.round(G)
    B = Math.round(B)

    var RR = ((R.toString(16).length==1)?"0"+R.toString(16):R.toString(16));
    var GG = ((G.toString(16).length==1)?"0"+G.toString(16):G.toString(16));
    var BB = ((B.toString(16).length==1)?"0"+B.toString(16):B.toString(16));

    return "#"+RR+GG+BB;
}