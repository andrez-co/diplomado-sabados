FROM nginx:alpine

# Copiar los archivos estáticos desde src/ al directorio web de Nginx
COPY src/index.html src/stile.css /usr/share/nginx/html/

# Exponer el puerto 80
EXPOSE 80

# Ejecutar Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]
