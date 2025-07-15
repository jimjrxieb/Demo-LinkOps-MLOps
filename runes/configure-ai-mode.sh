#!/bin/bash

# DEMO-LinkOps AI Mode Configuration Script
# This script helps you configure the platform to run with or without real AI capabilities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp env.template .env
fi

print_header "DEMO-LinkOps AI Mode Configuration"
echo ""
echo "This script helps you configure the platform's AI capabilities."
echo ""
echo "Available modes:"
echo "1. Demo Mode (default) - Simulated AI responses, no API costs"
echo "2. Real AI Mode - Connect to actual AI models (requires API keys)"
echo ""

# Function to set demo mode
set_demo_mode() {
    print_status "Configuring Demo Mode..."
    
    # Update .env file
    sed -i 's/^DEMO_MODE=.*/DEMO_MODE=true/' .env
    sed -i 's/^GROK_API_KEY=.*/# GROK_API_KEY=your_grok_api_key_here/' .env
    sed -i 's/^OPENAI_API_KEY=.*/# OPENAI_API_KEY=your_openai_api_key_here/' .env
    sed -i 's/^ANTHROPIC_API_KEY=.*/# ANTHROPIC_API_KEY=your_anthropic_api_key_here/' .env
    
    print_status "Demo mode configured successfully!"
    print_status "Features:"
    echo "  ✅ Full UI experience"
    echo "  ✅ Simulated AI responses"
    echo "  ✅ No API costs"
    echo "  ✅ Safe for demos"
    echo ""
}

# Function to set real AI mode
set_real_ai_mode() {
    print_status "Configuring Real AI Mode..."
    
    # Update demo mode setting
    sed -i 's/^DEMO_MODE=.*/DEMO_MODE=false/' .env
    
    echo ""
    echo "Select your preferred AI model:"
    echo "1. Grok (xAI)"
    echo "2. OpenAI (ChatGPT/GPT-4)"
    echo "3. Anthropic (Claude)"
    echo "4. Manual configuration"
    echo ""
    read -p "Enter your choice (1-4): " ai_choice
    
    case $ai_choice in
        1)
            read -p "Enter your Grok API key: " grok_key
            sed -i 's/^# GROK_API_KEY=.*/GROK_API_KEY='"$grok_key"'/' .env
            print_status "Grok API key configured!"
            ;;
        2)
            read -p "Enter your OpenAI API key: " openai_key
            sed -i 's/^# OPENAI_API_KEY=.*/OPENAI_API_KEY='"$openai_key"'/' .env
            print_status "OpenAI API key configured!"
            ;;
        3)
            read -p "Enter your Anthropic API key: " anthropic_key
            sed -i 's/^# ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY='"$anthropic_key"'/' .env
            print_status "Anthropic API key configured!"
            ;;
        4)
            print_status "Please manually edit the .env file to add your API keys."
            print_status "Then set DEMO_MODE=false to enable real AI capabilities."
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
    
    print_status "Real AI mode configured successfully!"
    print_warning "Remember to restart the platform:"
    echo "  docker-compose down"
    echo "  docker-compose up --build -d"
    echo ""
}

# Function to show current configuration
show_current_config() {
    print_header "Current Configuration"
    
    if [ -f ".env" ]; then
        echo "Environment file (.env) contents:"
        echo "----------------------------------------"
        grep -E "^(DEMO_MODE|GROK_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY)" .env || echo "No AI configuration found"
        echo "----------------------------------------"
    else
        print_warning "No .env file found"
    fi
    echo ""
}

# Main menu
while true; do
    echo "What would you like to do?"
    echo "1. Set Demo Mode (simulated AI)"
    echo "2. Set Real AI Mode (requires API keys)"
    echo "3. Show current configuration"
    echo "4. Exit"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            set_demo_mode
            break
            ;;
        2)
            set_real_ai_mode
            break
            ;;
        3)
            show_current_config
            ;;
        4)
            print_status "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please enter 1-4."
            echo ""
            ;;
    esac
done

print_header "Configuration Complete"
echo ""
print_status "Next steps:"
echo "1. If you changed to Real AI Mode, restart the platform:"
echo "   docker-compose down && docker-compose up --build -d"
echo ""
echo "2. If you're in Demo Mode, you can start immediately:"
echo "   docker-compose up -d"
echo ""
print_status "Configuration saved to .env file" 