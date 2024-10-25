import React, { useState } from 'react';
import { Container, Card, CardContent, Tabs, Tab, TextField, Button, Box } from '@mui/material';
import useApi from '../hooks/APIHandler'

function AuthScreen() {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const {callApi, error, loading} = useApi();
  // sending login form detail to the server
  const doLogin = async(e) => {
    e.preventDefault();
    let response = await callApi({url:"http://localhost:8000/api/auth/login/", method:"POST", body:{username:e.target.username.value, password:e.target.password.value}})
    console.log("data response: ", response);
  }
  // sending signup form detail to the server
  const doSignup = async(e) => {
    e.preventDefault();
    let response = await callApi({url:"http://localhost:8000/api/auth/signup/", method:"POST", body:{username:e.target.username.value, password:e.target.password.value, email:e.target.email.value, profile_pic: "https://media.istockphoto.com/id/1406197730/photo/portrait-of-a-young-handsome-indian-man.jpg?s=1024x1024&w=is&k=20&c=VruKKTu4jBF2xPEEQUMWwd4bwJPysSsqLuZ7h1OyD8M="}})
    console.log(response);
  }
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
                <TextField label="Username" name="username"  fullWidth margin="normal" variant="outlined" />
                <TextField label="Email" name="email" fullWidth margin="normal" variant="outlined" />
                <TextField label="Password" name="password" type="password" fullWidth margin="normal" variant="outlined" />
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