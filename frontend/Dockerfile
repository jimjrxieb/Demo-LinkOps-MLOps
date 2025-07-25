# ───────────────────────────────────────────────
# 🛠 Builder Stage: Install and build the app
# ───────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Clear npm cache and install dependencies
RUN npm cache clean --force && npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# ───────────────────────────────────────────────
# 🌐 NGINX Stage: Serve the app
# ───────────────────────────────────────────────
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/conf.d/default.conf.template

# Set default environment variables
ENV API_HOST=demo-unified-api
ENV API_PORT=9000

EXPOSE 3000

# Use a startup script to substitute environment variables
RUN apk add --no-cache bash
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"] 