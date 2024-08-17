import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MultiCloudDashboard from './components/MultiCloudDashboard';

const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <MultiCloudDashboard />
    </ThemeProvider>
  );
}

export default App;
