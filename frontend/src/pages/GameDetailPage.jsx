import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ArrowLeft } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export const GameDetailPage = () => {
  const { gameId } = useParams();
  const [game, setGame] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API_URL}/games/${gameId}`)
      .then(response => {
        setGame(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching game details:", err);
        setError("No se pudo cargar la información del juego.");
        setLoading(false);
      });
  }, [gameId]);

  if (loading) {
    return <div className="container mx-auto p-4 text-center">Cargando...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-4 text-center text-red-500">{error}</div>;
  }

  if (!game) {
    return null;
  }

  return (
    <div className="container mx-auto p-4 md:p-8">
      <Button asChild variant="outline" className="mb-6 bg-gray-800 hover:bg-gray-700">
        <Link to="/">
          <ArrowLeft className="mr-2 h-4 w-4" /> Volver a la lista
        </Link>
      </Button>

      <Card className="bg-gray-800 border-gray-700 text-white">
        <CardHeader>
          <CardTitle className="text-3xl md:text-4xl font-bold">{game.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <h2 className="text-2xl font-semibold mb-4 text-green-400">Comparativa de Precios</h2>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-600">
                <TableHead className="text-white">Tienda</TableHead>
                <TableHead className="text-white">Precio</TableHead>
                <TableHead className="text-white">Disponibilidad</TableHead>
                <TableHead className="text-white text-right">Enlace</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {game.prices.length > 0 ? (
                game.prices.map(price => (
                  <TableRow key={price.id} className="border-gray-700">
                    <TableCell className="font-medium">{price.store}</TableCell>
                    <TableCell>{price.price.toFixed(2)}€</TableCell>
                    <TableCell>
                      <span className={`px-2 py-1 rounded-full text-xs ${price.in_stock ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                        {price.in_stock ? 'En Stock' : 'Agotado'}
                      </span>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button asChild variant="ghost">
                        <a href={price.url} target="_blank" rel="noopener noreferrer">
                          Ir a la tienda
                        </a>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan="4" className="text-center text-gray-400">
                    No se encontraron precios para este juego.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};
