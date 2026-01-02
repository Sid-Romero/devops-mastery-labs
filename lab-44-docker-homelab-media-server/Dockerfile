# Use a lightweight base image
FROM nginx:alpine

# Copy a simple HTML file to serve as a placeholder
COPY index.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Command to start nginx
CMD ["nginx", "-g", "daemon off;"]