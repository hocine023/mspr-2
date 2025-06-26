import { useEffect, useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import Dashboard from './Dashboard';
import Graph from './Graph';
import 'leaflet/dist/leaflet.css';

function App() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    document.documentElement.classList.remove("light", "dark");
    document.documentElement.classList.add(theme);
  }, [theme]);

  return (
    <div className="min-h-screen bg-background text-foreground dark:bg-gray-900 dark:text-white transition-colors">
      {/* Bouton toggle thème */}
      <div className="flex justify-end p-4">
        <button
          className="px-4 py-2 rounded bg-gray-200 dark:bg-gray-700 text-black dark:text-white shadow"
          onClick={() => setTheme(theme === "light" ? "dark" : "light")}
        >
          {theme === "light" ? "🌙 Mode sombre" : "☀️ Mode clair"}
        </button>
      </div>

      <Dashboard />
    </div>
  );
}

export default App;
