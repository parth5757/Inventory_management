import React, { useState, useMemo, useEffect } from 'react';
import { Box, Card, CardContent, TextField, Button, CssBaseline, ThemeProvider, createTheme, Typography, LinearProgress } from '@mui/material';
import { ThemeProvider as Emotion10ThemeProvider } from '@emotion/react';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { orangeDarkTheme, orangeLightTheme, basicTheme, darkTheme, lightTheme, customTheme, blueLightTheme, blueDarkTheme, greenLightTheme, greenDarkTheme, redLightTheme, redDarkTheme } from '../layout/themes';
import { GlobalStyles } from '../layout/GlobalStyle';
import useAPI from '../hooks/APIHandler';
import OtpInput from 'react-otp-input';

const OTPVerifyPage = () => {
  const [otp, setOtp] = useState('');
  const [themeMode, setThemeMode] = useState('basic');
  const { callApi, loading } = useAPI();
  const navigate = useNavigate();

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

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    if (!otp) {
      toast.error('Please enter the OTP');
      return;
    }

    try {
      const response = await callApi({
        url: 'http://localhost:8000/api/auth/verify-otp/',
        method: 'POST',
        body: { otp },
      });

      if (response?.data?.success) {
        toast.success('OTP verified successfully!');
        navigate('/home');
      } else {
        toast.error('Invalid OTP. Please try again.');
      }
    } catch (err) {
      toast.error('An error occurred during OTP verification. Please try again.');
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
                Please enter the OTP sent to your registered phone number.
              </Typography>
              <Box component="form" sx={{ mt: 2 }} onSubmit={handleOtpSubmit}>
                {/* <TextField
                  label="OTP"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  fullWidth
                  margin="normal"
                  required
                /> */}
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
            <Box sx={{ textAlign: 'center', py: 2, borderTop: '1px solid', borderColor: theme.palette.divider }}>
              <Typography variant="body2" color="text.secondary">
                © 2024 My lekha Name. All rights reserved.
              </Typography>
            </Box>
          </Card>
        </Box>
      </ThemeProvider>
    </Emotion10ThemeProvider>
  );
};

export default OTPVerifyPage;
