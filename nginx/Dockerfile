FROM nginx:1.25-alpine

# Remove default configuration files
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/honeypot.conf /etc/nginx/conf.d/honeypot.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
