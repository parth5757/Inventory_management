import { isAuthenticated } from "./Helper"
import { Navigate } from "react-router-dom"
const ProtectedRoute=({element})=>{
    return isAuthenticated()?element:<Navigate to="/" />
}

export default ProtectedRoute;