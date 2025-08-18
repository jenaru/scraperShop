import { useState, useEffect } from 'react';
import axios from 'axios';
import { GameCard } from '../components/GameCard';
import { Input } from "@/components/ui/input";

const API_URL = 'http://localhost:8000'; // URL de tu backend FastAPI

export const GameListPage = () => {
  const [games, setGames] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    axios.get(`${API_URL}/games`)
      .then(response => setGames(response.data))
      .catch(error => console.error("Error fetching games:", error));
  }, []);

  const filteredGames = games.filter(game =>
    game.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="container mx-auto p-4 bg-gray-900 min-h-screen">
      <h1 className="text-4xl font-bold text-white mb-6">Comparador de Juegos</h1>
      <Input
        type="text"
        placeholder="Buscar juego..."
        className="mb-6 bg-gray-700 text-white border-gray-600"
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {filteredGames.map(game => (
          <GameCard key={game.id} game={game} />
        ))}
      </div>
    </div>
  );
};