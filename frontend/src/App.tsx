
import React, { useEffect } from 'react';
import { AppRouter } from './router/AppRouter';

function App() {
  useEffect(() => {
    // Aplicar tema guardado al cargar la aplicación
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, []);

  return <AppRouter />;
}

export default App;
