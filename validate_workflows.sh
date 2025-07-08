#!/bin/bash

echo "🔍 Validating GitHub Actions workflows and configurations..."

# Check YAML syntax for all workflow files
echo "📄 Checking YAML syntax..."
for workflow in .github/workflows/*.yml; do
    if python3 -c "import yaml; yaml.safe_load(open('$workflow'))" 2>/dev/null; then
        echo "✅ $(basename $workflow) - Valid YAML syntax"
    else
        echo "❌ $(basename $workflow) - Invalid YAML syntax"
        exit 1
    fi
done

# Check Docker Compose configuration
echo "🐳 Checking Docker Compose configuration..."
if docker-compose config --quiet; then
    echo "✅ docker-compose.yml - Valid configuration"
else
    echo "❌ docker-compose.yml - Invalid configuration"
    exit 1
fi

# Check frontend package.json
echo "📦 Checking frontend package.json..."
if cd frontend && npm list --depth=0 >/dev/null 2>&1; then
    echo "✅ Frontend dependencies - Valid"
    cd ..
else
    echo "❌ Frontend dependencies - Issues found"
    cd ..
fi

# Check required directories
echo "📂 Checking required directories..."
required_dirs=(
    "mlops/mlops_platform"
    "frontend/src/views"
    "shadows/kubernetes_specialist"
    "helm/linkops"
    ".github/workflows"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir - Directory exists"
    else
        echo "❌ $dir - Directory missing"
    fi
done

echo "🎉 Validation completed!"
echo ""
echo "🚀 Your workflows should now run successfully!"
echo "   - Push to main/develop branch to trigger CI/CD"
echo "   - Check GitHub Actions tab for workflow runs"
echo "   - Helm deployment is disabled until AKS is ready" 