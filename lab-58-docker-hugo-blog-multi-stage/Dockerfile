# Stage 1: Builder image
FROM klakegg/hugo:latest AS builder

WORKDIR /app

COPY . .

# Build the Hugo site
RUN hugo

# Stage 2: Final image (nginx)
FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Copy the built site from the builder stage
COPY --from=builder /app/public . 

# Optionally, customize the nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]