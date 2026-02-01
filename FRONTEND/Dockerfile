# Etapa de construcción
FROM node:18-alpine as build-stage

WORKDIR /app

# Copiar archivos de dependencias primero (mejor caché)
COPY package.json package-lock.json* ./

# Instalar dependencias (incluyendo chart.js y vue-chartjs)
RUN npm ci --legacy-peer-deps || npm install

# Copiar el resto del código
COPY . .

# Variables de entorno para el build
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Construir la aplicación
RUN npm run build

# Etapa de producción
FROM nginx:alpine as production-stage

# Copiar los archivos construidos desde la etapa anterior
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
