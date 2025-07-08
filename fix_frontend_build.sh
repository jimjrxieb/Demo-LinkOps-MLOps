#!/bin/bash

echo "🔧 Fixing LinkOps Frontend Build Issues..."

cd frontend

echo "📦 Cleaning npm cache and node_modules..."
rm -rf node_modules
rm -f package-lock.json
npm cache clean --force

echo "📥 Installing dependencies with Node.js 20 compatibility..."
npm install

echo "🧹 Cleaning dist directory..."
rm -rf dist

echo "🏗️ Building frontend..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Frontend build successful!"
    echo "🐳 Ready for Docker build"
else
    echo "❌ Frontend build failed!"
    exit 1
fi 