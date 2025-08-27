# GTM Engineering Blog - Dockerfile for Coolify deployment
FROM nginx:alpine

# Copy blog files to nginx document root
COPY . /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create necessary directories
RUN mkdir -p /usr/share/nginx/html/assets

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
  chmod -R 755 /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
