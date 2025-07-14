#!/bin/bash

# Substitute environment variables in NGINX config
envsubst '${API_HOST} ${API_PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# Start NGINX
exec nginx -g "daemon off;" 