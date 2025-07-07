#!/bin/bash

# LinkOps Platform Agent Build Script
# Builds the Go agent for multiple platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔨 Building LinkOps Platform Agent${NC}"
echo "====================================="

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo -e "${RED}❌ Go is not installed. Please install Go first.${NC}"
    exit 1
fi

# Get Go version
GO_VERSION=$(go version | awk '{print $3}')
echo -e "${GREEN}✅ Go version: $GO_VERSION${NC}"

# Create build directory
BUILD_DIR="build"
mkdir -p $BUILD_DIR

# Build for current platform
echo -e "${BLUE}🔨 Building for current platform...${NC}"
go build -o $BUILD_DIR/platform_agent platform_agent.go

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful for current platform${NC}"
else
    echo -e "${RED}❌ Build failed for current platform${NC}"
    exit 1
fi

# Cross-compilation targets
PLATFORMS=(
    "linux/amd64"
    "linux/arm64"
    "darwin/amd64"
    "darwin/arm64"
    "windows/amd64"
)

echo -e "${BLUE}🌍 Building for multiple platforms...${NC}"

for platform in "${PLATFORMS[@]}"; do
    IFS='/' read -r GOOS GOARCH <<< "$platform"
    
    echo -e "${YELLOW}Building for $GOOS/$GOARCH...${NC}"
    
    OUTPUT="$BUILD_DIR/platform_agent-$GOOS-$GOARCH"
    if [ "$GOOS" = "windows" ]; then
        OUTPUT="$OUTPUT.exe"
    fi
    
    GOOS=$GOOS GOARCH=$GOARCH go build -o "$OUTPUT" platform_agent.go
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Built: $OUTPUT${NC}"
    else
        echo -e "${RED}❌ Failed to build for $GOOS/$GOARCH${NC}"
    fi
done

# Create a simple test
echo -e "${BLUE}🧪 Creating test script...${NC}"
cat > $BUILD_DIR/test_agent.sh << 'EOF'
#!/bin/bash

echo "🧪 Testing Platform Agent..."

# Test help
echo "Testing help command..."
./platform_agent --help

# Test simple command
echo -e "\nTesting simple command..."
./platform_agent "echo 'Hello from Platform Agent'"

# Test rune execution
echo -e "\nTesting rune execution..."
if [ -f "../examples/system-info-rune.json" ]; then
    ./platform_agent --rune ../examples/system-info-rune.json
else
    echo "⚠️  Rune file not found, skipping rune test"
fi

echo -e "\n✅ Test completed!"
EOF

chmod +x $BUILD_DIR/test_agent.sh

# Create installation script
echo -e "${BLUE}📦 Creating installation script...${NC}"
cat > $BUILD_DIR/install.sh << 'EOF'
#!/bin/bash

# Installation script for Platform Agent

set -e

AGENT_NAME="platform_agent"
INSTALL_DIR="/usr/local/bin"

echo "🔧 Installing LinkOps Platform Agent..."

# Determine the correct binary for this platform
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

if [ "$ARCH" = "x86_64" ]; then
    ARCH="amd64"
elif [ "$ARCH" = "aarch64" ]; then
    ARCH="arm64"
fi

BINARY="$AGENT_NAME-$OS-$ARCH"

if [ "$OS" = "darwin" ]; then
    OS="darwin"
elif [ "$OS" = "linux" ]; then
    OS="linux"
else
    echo "❌ Unsupported operating system: $OS"
    exit 1
fi

if [ ! -f "$BINARY" ]; then
    echo "❌ Binary not found: $BINARY"
    echo "Available binaries:"
    ls -la $AGENT_NAME-*
    exit 1
fi

# Install the binary
sudo cp "$BINARY" "$INSTALL_DIR/$AGENT_NAME"
sudo chmod +x "$INSTALL_DIR/$AGENT_NAME"

echo "✅ Platform Agent installed to $INSTALL_DIR/$AGENT_NAME"

# Test installation
if command -v $AGENT_NAME &> /dev/null; then
    echo "✅ Installation verified"
    $AGENT_NAME --help
else
    echo "❌ Installation verification failed"
    exit 1
fi
EOF

chmod +x $BUILD_DIR/install.sh

# Create README
echo -e "${BLUE}📖 Creating README...${NC}"
cat > $BUILD_DIR/README.md << 'EOF'
# LinkOps Platform Agent

A production-ready Go CLI agent for safely executing shell commands and runes.

## Quick Start

### Install
```bash
cd build
./install.sh
```

### Test
```bash
cd build
./test_agent.sh
```

## Usage

### Single Command
```bash
platform_agent "kubectl get pods"
platform_agent "docker ps"
```

### Rune Execution
```bash
platform_agent --rune examples/deployment-rune.json
platform_agent --rune examples/system-info-rune.json
```

## Features

- ✅ Command validation and sanitization
- ✅ Timeout protection
- ✅ Comprehensive logging
- ✅ JSON result output
- ✅ Rune configuration support
- ✅ Cross-platform builds

## Safety

The agent includes multiple safety features:
- Path restrictions
- Command blacklisting
- Timeout limits
- Output capture
- Error handling

## Examples

See the `examples/` directory for sample rune configurations:
- `deployment-rune.json` - Kubernetes deployment
- `system-info-rune.json` - System information gathering
- `cleanup-rune.json` - Safe cleanup operations

## Build

To rebuild the agent:
```bash
./build.sh
```

## Platforms

Built for:
- Linux (amd64, arm64)
- macOS (amd64, arm64)
- Windows (amd64)
EOF

# Show build summary
echo -e "\n${GREEN}🎉 Build Complete!${NC}"
echo "=================="
echo -e "${BLUE}📁 Build directory: $BUILD_DIR${NC}"
echo -e "${BLUE}📦 Binaries created:${NC}"
ls -la $BUILD_DIR/platform_agent*

echo -e "\n${YELLOW}🚀 Next Steps:${NC}"
echo "1. cd $BUILD_DIR"
echo "2. ./test_agent.sh"
echo "3. ./install.sh (to install globally)"
echo "4. platform_agent --help"

echo -e "\n${GREEN}✅ Platform Agent is ready for use!${NC}" 