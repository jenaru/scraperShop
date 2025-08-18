import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { GameListPage } from './pages/GameListPage';
//import { GameDetailPage } from './pages/GameDetailPage'; // Necesitarás crear esta página
import './index.css'; // Asegúrate de que este archivo contiene las directivas de Tailwind

function App() {
  return (
    // 1. Envolvemos todo en el componente `Router` para habilitar la navegación
    <Router>
      {/* 2. Este `main` es el contenedor principal. Le aplicamos los estilos del modo oscuro. */}
      <main className="bg-gray-900 text-white min-h-screen font-sans antialiased">
        
        {/* 3. El componente `Routes` define dónde se renderizarán las diferentes páginas */}
        <Routes>

          {/* Ruta para la página principal: la lista de juegos */}
          <Route 
            path="/" 
            element={<GameListPage />} 
          />

          {/* Ruta para la página de detalle de un juego.
              ':gameName' es un parámetro dinámico. Cuando navegues a una URL como
              "/game/Catan", el componente GameDetailPage recibirá "Catan" como parámetro. */}
         {/*  <Route 
            path="/game/:gameName" 
            element={<GameDetailPage />} 
          /> */}
          
        </Routes>
      </main>
    </Router>
  );
}

export default App;