import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

import { motion } from "framer-motion";


export const GameCard = ({ game }) => {
  // Encuentra el precio más bajo para mostrarlo en la tarjeta
  const lowestPrice = Math.min(...game.prices.map(p => p.price));

  return (
    <motion.div whileHover={{ scale: 1.05 }}>
      <Card className="bg-gray-800 border-gray-700 text-white">
        <CardHeader>
          <CardTitle>{game.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Desde <span className="text-xl font-bold text-green-400">{lowestPrice}€</span></p>
          <p className="text-sm text-gray-400">{game.prices.length} tiendas</p>
        </CardContent>
      </Card>
    </motion.div>
  );
};