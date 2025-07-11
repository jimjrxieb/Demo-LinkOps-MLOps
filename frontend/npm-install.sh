# Clean and reinstall dependencies
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Build the frontend
npm run build
