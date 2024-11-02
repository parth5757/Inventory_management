import React, { useState, useEffect } from 'react';
import { Container, Card, CardContent, Tabs, Tab, TextField, Button, Box } from '@mui/material';
import PhoneInput from 'react-phone-input-2';
import 'react-phone-input-2/lib/material.css';
import useAPI from '../hooks/APIHandler';

function AuthScreen() {
  const[activeTab, setActiveTab] = useState(0);
  const[confirmPassword, setConfirmPassword] = useState('');
  const[errorMessage, setErrorMessage] = useState('');
  const[phone, setPhone] = useState('');
  const[profilePic, setProfilePic] = useState(null);
  const[signupSuccess, setSignupSuccess] = useState(false);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setErrorMessage('');
  };

  const { callApi, error, loading } = useAPI();

  const validatePhoneNumber = (phone) => {
    const formattedPhone = phone.replace(/^\+91/, ''); // Strip +91 for validation (I think it is not working this line.)
    return formattedPhone.length === 12 && /^\d+$/.test(formattedPhone); // 10 digits required after +91
  };

  const doLogin = async (e) => {
    e.preventDefault();
    let response = await callApi({
      url: "http://localhost:8000/api/auth/login/",
      method: "POST",
      body: {
        username: e.target.username.value,
        password: e.target.password.value
      }
    });
    console.log("data response: ", response);
  };

  const doSignup = async (e) => {
    e.preventDefault();
    const password = e.target.password.value;
    const confirmPasswordValue = e.target.confirmPassword.value;

    if (password !== confirmPasswordValue) {
      setErrorMessage("Passwords do not match");
      return;
    }
    
    if(!validatePhoneNumber(phone)){
      setErrorMessage("Phone number must have exactly 10 digits after +91");
      return;
    }

    // Use FormData to handle file upload for profile_pic
    const formData = new formData();
    formData.append("username", e.target.username.value);
    formData.append("email", e.target.email.value);
    formData.append("phone", `+${phone}`);
    formData.append("password", e.target.password.value);
    if(profilePic) formData.append("profile_pic", profilePic);
    
    const response = await callApi({
      url: "http://localhost:8000/api/auth/signup/",
      method: "POST",
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    if (error) {
      setErrorMessage(error);
    } else if (response && response.data) {
      console.log("Signup response: ", response.data);
      setSignupSuccess(true);
    }
  };

  // Redirect to login tab on successful signup

  useEffect(() => {
    if (signupSuccess) {
      setActiveTab(0); // Switch to login tab
      setSignupSuccess(false); // Reset signup success flag
      setErrorMessage(''); // Clear any error messages
    }
  }, [signupSuccess]);
  return (
    <Container maxWidth="sm" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
      <Card>
        <CardContent>
          <Tabs value={activeTab} onChange={handleTabChange} centered>
            <Tab label="Login" />
            <Tab label="Sign Up" />
          </Tabs>

          {activeTab === 0 && (
            <Box sx={{ mt: 2 }}>
              <h2>Login</h2>
              <form onSubmit={doLogin}>
                <TextField label="Username" name="username" fullWidth margin="normal" variant="outlined" />
                <TextField label="Password" name="password" type="password" fullWidth margin="normal" variant="outlined" />
                <Button variant="contained" color="primary" fullWidth type="submit">Login</Button>
              </form>
            </Box>
          )}

          {activeTab === 1 && (
            <Box sx={{ mt: 2 }}>
              <h2>Sign Up</h2>
              <form onSubmit={doSignup}>
                <TextField label="Username" name="username" fullWidth margin="normal" variant="outlined" />
                <TextField label="Email" name="email" fullWidth margin="normal" variant="outlined" />
                <PhoneInput
                  country={'in'}
                  onlyCountries={['in']}
                  value={phone}
                  onChange={(value) => setPhone(value)}
                  inputStyle={{
                    width: '100%',
                    paddingLeft: '50px',
                    paddingTop: '18.5px',
                    paddingBottom: '18.5px',
                    marginTop: '16px',
                    marginBottom: '8px',
                    borderRadius: '4px',
                    fontSize: '16px',
                  }}
                  containerStyle={{ width: '100%' }}
                  // disableCountryCode
                  // disableDropdown
                  specialLabel=''
                  placeholder="Enter 10-digit phone number"
                />
                <TextField label="Password" name="password" type="password" fullWidth margin="normal" variant="outlined" />
                <TextField
                  label="Confirm Password"
                  name="confirmPassword"
                  type="password"
                  fullWidth
                  margin="normal"
                  variant="outlined"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
                {/* Profile Picture Input */}
                <TextField
                  type="file"
                  fullWidth
                  margin="normal"
                  variant="outlined"
                  onChange={(e) => setProfilePic(e.target.files[0])}
                />
                {errorMessage && <Box sx={{ color: 'red', mt: 1 }}>{errorMessage}</Box>}
                <Button variant="contained" color="primary" fullWidth type="submit">Sign Up</Button>
              </form>
            </Box>
          )}
        </CardContent>
      </Card>
    </Container>
  );
}

export default AuthScreen;






// import React, { useState, useEffect } from 'react';
// import { Container, Card, CardContent, Tabs, Tab, TextField, Button, Box } from '@mui/material';
// import PhoneInput from 'react-phone-input-2';
// import 'react-phone-input-2/lib/material.css'; // Import Material theme for react-phone-input-2
// import useApi from '../hooks/APIHandler';

// function AuthScreen() {
//   const [activeTab, setActiveTab] = useState(0);
//   const [confirmPassword, setConfirmPassword] = useState('');
//   const [errorMessage, setErrorMessage] = useState('');
//   const [phone, setPhone] = useState('');
//   const [signupSuccess, setSignupSuccess] = useState(false);

//   const handleTabChange = (event, newValue) => {
//     setActiveTab(newValue);
//     setErrorMessage(''); // Reset error message on tab switch
//   };

//   const { callApi, error, loading } = useApi();

//   const validatePhoneNumber = (phone) => {
//     const formattedPhone = phone.replace(/^\+91/, ''); // Strip +91 for validation
//     return formattedPhone.length === 12 && /^\d+$/.test(formattedPhone); // 10 digits required after +91
//   };

//   const doLogin = async (e) => {
//     e.preventDefault();
//     let response = await callApi({
//       url: "http://localhost:8000/api/auth/login/",
//       method: "POST",
//       body: {
//         username: e.target.username.value,
//         password: e.target.password.value
//       }
//     });
//     console.log("data response: ", response);
//   };

//   const doSignup = async (e) => {
//     e.preventDefault();
//     const password = e.target.password.value;
//     const confirmPasswordValue = e.target.confirmPassword.value;

//     if (password !== confirmPasswordValue) {
//       setErrorMessage("Passwords do not match");
//       return;
//     }

//     if (!validatePhoneNumber(phone)) {
//       setErrorMessage("Phone number must have exactly 10 digits after +91");
//       return;
//     }

//     const response = await callApi({
//       url: "http://localhost:8000/api/auth/signup/",
//       method: "POST",
//       body: {
//         username: e.target.username.value,
//         email: e.target.email.value,
//         phone: `+${phone}`, // Add "+" before the phone number
//         password: password,
//       }
//     });

//     if (error) {
//       setErrorMessage(error);
//     } else if (response && response.data) {
//       console.log("Signup response: ", response.data);
//     }
//   };
//   // Redirect to login tab on successful signup
//   useEffect(() => {
//   if (signupSuccess) {
//     setActiveTab(0); // Switch to login tab
//     setSignupSuccess(false); // Reset signup success flag
//     setErrorMessage(''); // Clear any error messages
//   }
//   }, [signupSuccess]);

//   return (
//     <Container maxWidth="sm" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
//       <Card>
//         <CardContent>
//           <Tabs value={activeTab} onChange={handleTabChange} centered>
//             <Tab label="Login" />
//             <Tab label="Sign Up" />
//           </Tabs>

//           {activeTab === 0 && (
//             <Box sx={{ mt: 2 }}>
//               <h2>Login</h2>
//               <form onSubmit={doLogin}>
//                 <TextField label="Username" name="username" fullWidth margin="normal" variant="outlined" required />
//                 <TextField label="Password" name="password" type="password" fullWidth margin="normal" variant="outlined" required />
//                 <Button variant="contained" color="primary" fullWidth type="submit">Login</Button>
//               </form>
//             </Box>
//           )}

//           {activeTab === 1 && (
//             <Box sx={{ mt: 2 }}>
//               <h2>Sign Up</h2>
//               <form onSubmit={doSignup}>
//                 <TextField label="Username" name="username" fullWidth margin="normal" variant="outlined" required/>
//                 <TextField label="Email" name="email" fullWidth margin="normal" variant="outlined" required/>
//                 <PhoneInput
//                   country={'in'}
//                   onlyCountries={['in']}
//                   value={phone}
//                   onChange={(value) => setPhone(value)}
//                   inputStyle={{
//                     width: '100%',
//                     paddingLeft: '50px',
//                     paddingTop: '18.5px',
//                     paddingBottom: '18.5px',
//                     marginTop: '16px',
//                     marginBottom: '8px',
//                     borderRadius: '4px',
//                     fontSize: '16px',
//                   }}
//                   containerStyle={{ width: '100%' }}
//                   // disableCountryCode
//                   // disableDropdown
//                   specialLabel = ""
//                   placeholder="Enter 10-digit phone number"
//                 />
//                 <TextField label="Password" name="password" type="password" fullWidth margin="normal" variant="outlined" />
//                 <TextField
//                   label="Confirm Password"
//                   name="confirmPassword"
//                   type="password"
//                   fullWidth
//                   margin="normal"
//                   variant="outlined"
//                   value={confirmPassword}
//                   onChange={(e) => setConfirmPassword(e.target.value)}
//                 />
//                 {errorMessage && <Box sx={{ color: 'red', mt: 1 }}>{errorMessage}</Box>}
//                 <Button variant="contained" color="primary" fullWidth type="submit">Sign Up</Button>
//               </form>
//             </Box>
//           )}
//         </CardContent>
//       </Card>
//     </Container>
//   );
// }

// export default AuthScreen;
