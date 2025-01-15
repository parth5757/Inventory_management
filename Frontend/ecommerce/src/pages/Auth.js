// Refer official theme auth.js for feature need
// Auth.js
import React, { useState, useMemo, useEffect } from 'react';
import { Tabs, Tab, Card, CardContent, Typography, TextField, Button, Box, CssBaseline, ThemeProvider, createTheme, LinearProgress } from '@mui/material';
import { ThemeProvider as Emotion10ThemeProvider } from '@emotion/react';
import PhoneInput from 'react-phone-input-2';
import 'react-phone-input-2/lib/material.css';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { orangeDarkTheme, orangeLightTheme, basicTheme, darkTheme, lightTheme, customTheme, blueLightTheme, blueDarkTheme, greenLightTheme, greenDarkTheme, redLightTheme, redDarkTheme } from '../layout/themes';
import { GlobalStyles } from '../layout/GlobalStyle';
import useAPI from '../hooks/APIHandler';

const Auth = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [confirmPassword, setConfirmPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [profilePic, setProfilePic] = useState(null);
  const [themeMode, setThemeMode] = useState('basic');
  const [signupSuccess, setSignupSuccess] = useState(false);
  const navigate = useNavigate();
  const { callApi, error, loading  } = useAPI();

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'basic';
    setThemeMode(savedTheme);
  }, []);

  const theme = useMemo(() => {
    switch (themeMode) {
      case 'basic':
        return createTheme(basicTheme);
      case 'dark':
        return createTheme(darkTheme);
      case 'light':
        return createTheme(lightTheme);
      case 'custom':
        return createTheme(customTheme);
      case 'blue light':
        return createTheme(blueLightTheme);
      case 'blue dark':
        return createTheme(blueDarkTheme);
      case 'green light':
        return createTheme(greenLightTheme);
      case 'green dark':
        return createTheme(greenDarkTheme);
      case 'red light':
        return createTheme(redLightTheme);
      case 'red dark':
        return createTheme(redDarkTheme);
      case 'orange light':
        return createTheme(orangeLightTheme);
      case 'orange dark':
        return createTheme(orangeDarkTheme);
      default:
        return createTheme(lightTheme);
    }
  }, [themeMode]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const validatePhoneNumber = (phone) => {
    const formattedPhone = phone.replace(/^\+91/, '');
    return formattedPhone.length === 12 && /^\d+$/.test(formattedPhone);
  };

  const doLogin = async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;

    if (!username || !password) {
      toast.error("Username and password are required");
      return;
    }

    try {
      const response = await callApi({
        url: "http://localhost:8000/api/auth/login/",
        method: "POST",
        body: { username, password },
      });

      if (response?.data?.access) {
        localStorage.setItem("token", response.data.access);
        toast.success("Login successful!");
        navigate("/home");
      } else {
         toast.error(response.data.error);
      }
    } catch (err) {
      toast.error(err);
      toast.error("An error occurred. Please try again.");
    }
  };

  const doSignup = async (e) => {
    e.preventDefault();
    const password = e.target.password.value;
    const confirmPasswordValue = e.target.confirmPassword.value;

    if (password !== confirmPasswordValue) {
      toast.error("Passwords do not match");
      return;
    }

    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
    if (!passwordRegex.test(password)) {
      toast.error("Password must be 8-16 characters long and include at least one uppercase letter, one lowercase letter, one numeric digit, and one special character.");
      return;
    }

    if (!validatePhoneNumber(phone)) {
      toast.error("Phone number must have exactly 10 digits after +91");
      return;
    }

    const email = e.target.email.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      toast.error("Please enter a valid email address");
      return;
    }

    const formData = new FormData();
    formData.append("username", e.target.username.value);
    formData.append("email", email);
    formData.append("phone", `+${phone}`);
    formData.append("password", password);
    if (profilePic) formData.append("profile_pic", profilePic);

    try {
      const response = await callApi({
        url: "http://localhost:8000/api/auth/signup/",
        method: "POST",
        body: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (response?.data?.error === "Username not available") {
        toast.error("Username not available.");f
        const suggestions = response.data.suggestions;
        if (suggestions?.length > 0) {
          toast.info(`Suggested usernames: ${suggestions.join(", ")}`);
        }
      } else if (response?.data) {
        localStorage.setItem("ET", response.data.access);
        toast.success("Signup successful");
        setSignupSuccess(true);
      } else {
        toast.error("Signup failed, please try again", error);
      }
    } catch (err) {
      const errorMessage = err?.response?.data?.error || "An error occurred during signup";
      toast.error(errorMessage);
    }
  };

  useEffect(() => {
    if (signupSuccess) {
      setActiveTab(0); //remove this only navigate is required
      setSignupSuccess(false);
      navigate("/verify"); // directly navigate to the verify page
    }
  }, [signupSuccess]);

  return (
    <Emotion10ThemeProvider theme={theme}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <GlobalStyles />
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: theme.palette.background.default }}>
          <Card sx={{ maxWidth: 500, width: '100%' }}>
            <CardContent>
              <Tabs value={activeTab} onChange={handleTabChange} centered>
                <Tab label="Login" />
                <Tab label="Sign Up" />
              </Tabs>

              {activeTab === 0 && (
                <Box component="form" sx={{ mt: 2 }} onSubmit={doLogin}>
                  <TextField label="Username" name="username" fullWidth margin="normal" required />
                  <TextField label="Password" name="password" type="password" fullWidth margin="normal" required />
                  {loading?<LinearProgress sx={{width:'100%'}}/>:<Button variant="contained" color="primary" fullWidth type="submit" sx={{ mt: 2 }}>Login</Button>}
                </Box>
              )}

              {activeTab === 1 && (
                <Box component="form" sx={{ mt: 2 }} onSubmit={doSignup}>
                  <TextField label="Username" name="username" fullWidth margin="normal" required />
                  <TextField label="Email" name="email" fullWidth margin="normal" required />
                  <PhoneInput country={'in'} onlyCountries={['in']} value={phone} onChange={setPhone} inputStyle={{ width: '100%' }} />
                  <TextField label="Password" name="password" type="password" fullWidth margin="normal" required />
                  <TextField label="Confirm Password" name="confirmPassword" type="password" fullWidth margin="normal" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
                  <TextField type="file" fullWidth margin="normal" onChange={(e) => setProfilePic(e.target.files[0])} />
                  {loading?<LinearProgress sx={{width:'100%'}}/>:<Button variant="contained" color="primary" fullWidth type="submit" sx={{ mt: 2 }}>Sign Up</Button>}
                </Box>
              )}
            </CardContent>
            <Box sx={{ textAlign: 'center', py: 2, borderTop: '1px solid', borderColor: theme.palette.divider }}>
              <Typography variant="body2" color="text.secondary">© 2024 lekha All rights reserved.</Typography>
            </Box>
          </Card>
        </Box>
      </ThemeProvider>
    </Emotion10ThemeProvider>
  );
};

export default Auth;
