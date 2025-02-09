import React, { useState, useMemo, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Button, CssBaseline, ThemeProvider, createTheme, LinearProgress } from '@mui/material';
import { ThemeProvider as Emotion10ThemeProvider } from '@emotion/react';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { orangeDarkTheme, orangeLightTheme, basicTheme, darkTheme, lightTheme, customTheme, blueLightTheme, blueDarkTheme, greenLightTheme, greenDarkTheme, redLightTheme, redDarkTheme } from '../layout/themes';
import { GlobalStyles } from '../layout/GlobalStyle';
import useAPI from '../hooks/APIHandler';
import OtpInput from 'react-otp-input';
import { getEmail } from '../utils/Helper'

const OTPVerifyPage = () => {
  const [otp, setOtp] = useState('');
  const [email, setEmail] = useState(''); // State to store session email 
  const [themeMode, setThemeMode] = useState('basic');
  const [timer, setTimer] = useState(5);
  const [resendDisabled, setResendDisabled] = useState(true);
  const { callApi, loading } = useAPI();
  const navigate = useNavigate();

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'basic';
    setThemeMode(savedTheme);
    

    // Fetch email from session
    const fetchTokenEmail = async () => {
      try {
        //  This is for session decode email which not working currently getting from jwt token
        // const response = await callApi({
        //   url: 'http://localhost:8000/api/auth/verify-email/', // Backend endpoint to fetch session email
        //   method: 'POST',
        // });

        // if (response?.data?.email) {
        //   alert(response?.data?.email)
        //   setEmail(response.data.email); // Set the session email in state
        // }
        // // else take from jwt token email 
        // else {
          setEmail(getEmail().email)
        // } 
        // else {
        //   toast.error('Failed to fetch session email.');
        // }
      } catch (err) {
        toast.error('An error occurred while fetching email.');
      }
    };
    // check if email already fetch from server then not send request again 
    if (email.length == 0){
      fetchTokenEmail();
    }
  }, [callApi]);

  useEffect(() => {
    let interval;
    if(timer > 0) {
      interval = setInterval(() => {
        setTimer((prevTimer) => prevTimer-1);
      }, 1000);
    }else{
      setResendDisabled(false);
    }
    return () => clearInterval(interval);
  }, [timer]);

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

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    if (!otp) {
      toast.error('Please enter the OTP');
      return;
    }

    try {
      const response = await callApi({
        url: 'http://localhost:8000/api/auth/verify-email/',
        method: 'POST',
        body: { otp, email },
      });

      console.log("the response is:", response?.data);
      if (response?.data?.verified) {
        toast.success('Email verified successfully!');
        navigate('/auth');
      } else {
        toast.error('Invalid OTP. Please try again.');
      }
    } catch (err) {
      toast.error('An error occurred during OTP verification. Please try again.');
    }
  };

  const handleResendOTP = async () => {
    setResendDisabled(true);
    setTimer(120);
    try {
      const response = await callApi({
        url: 'http://localhost:8000/api/auth/resend-otp/',
        method: 'POST',
        body: { email },
      });

      if (response?.data?.success) {
        toast.success('OTP resent successfully!');
      } else {
        toast.error('Failed to resend OTP. Please try again.');
      }
    } catch (err) {
      toast.error('An error occurred while resending OTP.');
    }
  };

  return (
    <Emotion10ThemeProvider theme={theme}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <GlobalStyles />
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: theme.palette.background.default }}>
          <Card sx={{ maxWidth: 400, width: '100%' }}>
            <CardContent>
              <Typography variant="h5" component="div" gutterBottom>
                OTP Verification
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Please enter the OTP sent to your registered email.
              </Typography>
              {/* Dynamically display the email */}
              <Typography variant="body2" color="text.secondary">
                Email: <strong>{email || 'Loading...'}</strong>
              </Typography>
              <Box component="form" sx={{ mt: 2 }} onSubmit={handleOtpSubmit}>
                {/* Hidden input field to pass the email */}
                <input type="hidden" name="email" value={email} />
                <Typography
                  variant="body2"
                  sx={{ mt: 1, textDecoration: 'underline', color: theme.palette.primary.main, cursor: 'pointer' }}
                >
                  Change Email
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <OtpInput
                    value={otp}
                    onChange={setOtp}
                    numInputs={6}
                    renderSeparator={<span>&nbsp;&nbsp;</span>}
                    renderInput={(props) => (
                      <input
                        {...props}
                        style={{
                          width: '100%',
                          padding: '20px',
                          textAlign: 'center',
                          borderRadius: '16px',
                          border: `3px solid ${theme.palette.divider}`,
                        }}
                      />
                    )}
                  />
                </Box>
                {loading ? (
                  <LinearProgress sx={{ width: '100%' }} />
                ) : (
                  <Button variant="contained" color="primary" fullWidth type="submit" sx={{ mt: 2 }}>
                    Verify OTP
                  </Button>
                )}
              </Box>
            </CardContent>
            {/* Timer & Resend Button */}
            <Box sx={{ textAlign: 'center', py:2}}>
              {resendDisabled ?(
                <Typography variant="body" color="text.secondary">
                  You can request for new otp in {timer} seconds
                  <br />
                </Typography>
              ) : (
                <Typography variant="body" color="text.secondary">
                  You can now request to another otp
                  <br />
                </Typography>
              )}
              {resendDisabled ?(
                <Button disabled={true} variant="contained" color="primary" onClick={handleResendOTP}>
                  Resend OTP
                </Button>
              ) : (
                <Button disabled={false} variant="contained" color="primary" onClick={handleResendOTP}>
                  Resend OTP
                </Button>
              )}
            </Box>
            {/* Copyrights */}
            <Box sx={{ textAlign: 'center', py: 2, borderTop: '1px solid', borderColor: theme.palette.divider }}>
              <Typography variant="body2" color="text.secondary">
                © 2025 lekha.dev. All rights reserved.
              </Typography>
            </Box>
          </Card>
        </Box>
      </ThemeProvider>
    </Emotion10ThemeProvider>
  );
};

export default OTPVerifyPage;
