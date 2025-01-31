import { jwtDecode } from 'jwt-decode';


export const Authenticate = () => {
    const token = localStorage.getItem("token")
    const ET = localStorage.getItem("ET");
    if(ET){
        localStorage.removeItem("ET");   
    } 
    // this check that toke exist if yes then check expiry if expiry then delete the token
    if(token){
        const decodedToken = jwtDecode(token);
        const currentTime = Date.now()/1000
        if(decodedToken.exp<currentTime){
            localStorage.removeItem("token");
        }
        if(decodedToken.exp>currentTime){
            return false 
        }
    }
    else{
        return true
    }
}
 
export const isVerify = () => {
    const ET = localStorage.getItem("ET");
    const token = localStorage.getItem("token");
    if(token){
        localStorage.removeItem("token");
    }
    if(ET){
        return true;
    }
}

export const isAuthenticated =()=> {
    const token = localStorage.getItem("token");
    const ET = localStorage.getItem("ET");
    if(ET){
        localStorage.removeItem("ET")
    }
    if(!token){
        return false;
    }
    try{
        const decodedToken = jwtDecode(token);
        const currentTime = Date.now()/1000
        if(decodedToken.exp<currentTime){
            localStorage.removeItem("token");
        }
        return decodedToken.exp>currentTime
    }
    catch(err){
        return false;
    }
}

//  get user detail from jwt token
export const getUser=()=>{
    const token = localStorage.getItem("token");
    if(!token){
        return null;
    }
    try{
        const decodedToken=jwtDecode(token);
        return decodedToken
    }
    catch(err){
        return null;
    }
}

// get unverified user email for otp verification
export const getEmail=()=>{
    const ET = localStorage.getItem("ET");
    if(!ET){
        return null;
    }
    try{
        const decodedToken=jwtDecode(ET);
        return decodedToken
    }
    catch(err){
        return null;
    }
}