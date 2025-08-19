import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { GameListPage } from './pages/GameListPage';
import { GameDetailPage } from './pages/GameDetailPage'; // Se importará la nueva página
import './index.css';

function App() {
  return (
    <Router>
      <main className="bg-gray-900 text-white min-h-screen font-sans antialiased">
        <Routes>
          {/* Ruta para la página principal (lista de juegos) */}
          <Route 
            path="/" 
            element={<GameListPage />} 
          />

          {/* Ruta para la página de detalle, usando el ID del juego */}
          <Route
            path="/game/:gameId"
            element={<GameDetailPage />} 
          />
          
        </Routes>
      </main>
    </Router>
  );
}

export default App;