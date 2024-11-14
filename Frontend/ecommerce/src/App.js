// Custom Internal library
import './App.css';
import Layout from './layout/layout';
import Home from './pages/Home';
import AuthScreen from './pages/AuthScreen';
import ProtectedRoute from './utils/ProtectedRoute';
// react router dom library
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const sidebarItems=[
  {name: "Home", link:"/home", icon:"home"},
  {name:"Products", link: "/products", icon: "products"},
  {name:"Categories", icon:"categories", children:[{name:"All Categories", link:"/categories"}, {name:"Add  Category", link:"/categories/add"}]},
  {name: "Orders", link: "/orders", icon: "orders"},
  {name: "Users", link: "/users", icon: "users"},
  {name:"Settings",link:"/settings",icon:"settings"},
]


const router = createBrowserRouter(
  [
    {path:"/auth", element:<AuthScreen />},
    {
      path:"/",
      element:<Layout sidebarList={sidebarItems}/>,
      children:[
        {path:"home", element:<ProtectedRoute element={<Home />} />}
      ]},
  ]
)

function App(){
  return(
    <>
      <RouterProvider router={router} /> 
      <ToastContainer position="bottom-right" autoClose={8000} hideProgressBar={false} style={{ marginBottom: '30px' }} />
    </>
  )
}
export default App;