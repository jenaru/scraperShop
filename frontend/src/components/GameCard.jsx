import { Link } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";

export const GameCard = ({ game }) => {
  // Manejar el caso donde no hay precios para evitar errores
  const lowestPrice = game.prices.length > 0
    ? Math.min(...game.prices.map(p => p.price))
    : null;

  return (
    <Link to={`/game/${game.id}`} className="no-underline">
      <motion.div whileHover={{ scale: 1.05 }} className="h-full">
        <Card className="bg-gray-800 border-gray-700 text-white h-full flex flex-col justify-between">
          <CardHeader>
            <CardTitle>{game.name}</CardTitle>
          </CardHeader>
          <CardContent>
            {lowestPrice !== null ? (
              <>
                <p>Desde <span className="text-xl font-bold text-green-400">{lowestPrice.toFixed(2)}€</span></p>
                <p className="text-sm text-gray-400">{game.prices.length} tienda(s)</p>
              </>
            ) : (
              <p className="text-gray-400">No hay precios disponibles</p>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </Link>
  );
};