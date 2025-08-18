import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from "path" // <--- ¡ESTA ES LA LÍNEA QUE FALTA!


export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      // Aquí está la magia:
      // Le decimos a Vite que cada vez que vea '@',
      // debe apuntar a la carpeta 'src' de nuestro proyecto.
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
