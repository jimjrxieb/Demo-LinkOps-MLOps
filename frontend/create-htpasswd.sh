#!/bin/bash

# Create htpasswd file for Basic Auth
# Username: demo
# Password: KubernetesCD2024!

echo "Creating htpasswd file for demo access..."
htpasswd -cb .htpasswd demo KubernetesCD2024!

echo "✅ htpasswd file created successfully!"
echo "Username: demo"
echo "Password: KubernetesCD2024!"
echo ""
echo "To change the password, run:"
echo "htpasswd .htpasswd demo" 