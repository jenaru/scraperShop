# --- Etapa 1: Build ---
# Usa una imagen oficial de Node.js como base.
FROM node:18-alpine AS build

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copia los archivos de manifiesto del proyecto (package.json y package-lock.json).
# Usar `COPY` selectivo aprovecha el cache de Docker si no hay cambios en las dependencias.
COPY package*.json ./

# Instala las dependencias del proyecto.
RUN npm install

# Copia el resto del código fuente de la aplicación.
COPY . .

# Construye la aplicación para producción.
# El resultado se guardará en el directorio /app/dist.
RUN npm run build

# --- Etapa 2: Serve ---
# Usa una imagen ligera de Nginx para servir el contenido.
FROM nginx:1.25-alpine

# Copia la configuración personalizada de Nginx.
# Esto es crucial para que las rutas de React Router funcionen correctamente.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia los archivos estáticos construidos en la etapa anterior.
# Los serviremos desde el directorio raíz de Nginx.
COPY --from=build /app/dist /usr/share/nginx/html

# Expone el puerto 80 para que el contenedor pueda recibir tráfico.
EXPOSE 80

# El comando por defecto de Nginx ya es iniciar el servidor,
# por lo que no necesitamos un CMD explícito.
CMD ["nginx", "-g", "daemon off;"]
