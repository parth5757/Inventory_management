import { isAuthenticated, Authenticate, isVerify } from "./Helper"
import { Navigate } from "react-router-dom"
const ProtectedRoute=({element})=>{
    const authenticatedPages = ["Home", "Inventory", "Purchase", "Order", "Invoice", "Customer"];
    // check the element name as per the current page and according to that check there different custom function records
    // this is for the if request for home page or any other page
    if (authenticatedPages.includes(element.type.name)){
        return isAuthenticated()?element:<Navigate to="/auth" />
    }
    // this is at auth page if user authenticate come to login it don't allow to stay at that page 
    else if(element.type.name === "Auth"){
        console.log("auth url route")
        return Authenticate()?element:<Navigate to="/home" />
    }
    // this is at otp verification at there only ET token allowed not any other 
    else if(element.type.name === "OTPVerifyPage"){
        console.log("i am at otp")
        return isVerify()?element:<Navigate to="/auth" />
    }
}
export default ProtectedRoute;