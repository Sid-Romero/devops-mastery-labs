# Layer 0 : Base image
FROM node:18-slim

# Layer 1 : Set working directory
WORKDIR /usr/src/app

 # Layer 2 : specify dependencies
COPY package.json package-lock.json ./

# Layer 3 : Install app dependencies (excluding dev dependencies)
RUN npm install --omit=dev

# Layer 4 : Copy app source code
COPY . .

# Layer 5 : non-root user (security best practice)
USER node

# Expose port used in the app
EXPOSE 8080

 # Entrypoint
CMD ["node", "server.js"]

