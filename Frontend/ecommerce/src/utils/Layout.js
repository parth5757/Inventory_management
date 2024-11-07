import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Layout = ({ children }) => {
  return (
    <>
      {children}
      <ToastContainer 
        position="bottom-right" 
        autoClose={8000} 
        hideProgressBar={false} 
        style={{ marginBottom: '30px' }}
      />
    </>
  );
};

export default Layout;