// Custom Internal library
import './App.css';
import Layout from './utils/Layout';
import Home from './pages/Home';
import AuthScreen from './pages/AuthScreen';
import ProtectedRoute from './utils/ProtectedRoute';
// react router dom library
import {createBrowserRouter, RouterProvider} from 'react-router-dom';

const router = createBrowserRouter(
  [
    {path:"/", element:<AuthScreen />},
    {path:"/home", element:<ProtectedRoute element={<Home />}/>},
    // {path:"/home", element:<Home />}
  ]
)

function App(){
  return(
    <Layout>
      <RouterProvider router={router} /> 
    </Layout>    
  )
}
export default App;