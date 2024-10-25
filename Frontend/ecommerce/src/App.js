import './App.css';
import Layout from './utils/Layout';
import Home from './pages/Home';
import AuthScreen from './pages/AuthScreen';
import {createBrowserRouter, RouterProvider} from 'react-router-dom';

const router = createBrowserRouter(
  [
    {path:"/", element:<AuthScreen />},
    {path:"/home/", element:<Home />},
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