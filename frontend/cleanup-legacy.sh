#!/bin/bash

echo "🔍 Cleaning up legacy Vue components..."

# Remove legacy James components
rm -f src/views/JamesGUI.vue
rm -f src/views/DashboardView.vue
rm -f src/components/JamesGUI.vue
rm -f src/components/JamesHeader.vue
rm -f src/components/JamesFooter.vue
rm -f src/components/JamesForm.vue
rm -f src/components/JamesLogicFlow.vue

# Remove other legacy components that might conflict
rm -f src/components/DemoBanner.vue
rm -f src/components/StoreExample.vue
rm -f src/components/AuditInput.vue
rm -f src/components/AuditPanel.vue
rm -f src/components/AuditResults.vue
rm -f src/components/FicknurySearch.vue
rm -f src/components/OrbCard.vue
rm -f src/components/RuneCard.vue
rm -f src/components/Dashboard.vue
rm -f src/components/WhisFlow.vue

# Remove legacy views that aren't part of the new admin dashboard
rm -f src/views/Whis.vue
rm -f src/views/Dashboard.vue
rm -f src/views/Login.vue
rm -f src/views/Audit.vue
rm -f src/views/NotFound.vue

echo "✅ Removed old legacy components."

# Clean router - remove any references to deleted components
sed -i '/JamesGUI/d' src/router/index.js
sed -i '/DashboardView/d' src/router/index.js
sed -i '/Whis.vue/d' src/router/index.js
sed -i '/Dashboard.vue/d' src/router/index.js
sed -i '/Login.vue/d' src/router/index.js
sed -i '/Audit.vue/d' src/router/index.js
sed -i '/NotFound.vue/d' src/router/index.js

echo "✅ Cleaned up router imports."

# Verify the router only has the new admin dashboard routes
echo "📋 Current router routes:"
grep -E "path:|component:" src/router/index.js

echo ""
echo "🧹 Cleanup completed!"
echo "📦 Next steps:"
echo "  1. Run: npm run lint --fix"
echo "  2. Run: npm run build"
echo "  3. Test the application" 