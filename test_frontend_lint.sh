#!/bin/bash

echo "🔍 Testing frontend linting..."

cd frontend

echo "📦 Installing/updating dependencies..."
npm ci --silent

echo "🧹 Running ESLint..."
npm run lint

echo "🏗️ Testing build..."
npm run build

echo "✅ Frontend tests completed!" 