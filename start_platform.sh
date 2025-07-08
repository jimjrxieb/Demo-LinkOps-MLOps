#!/bin/bash

# LinkOps MLOps Platform Startup Script
# Automatically starts all services in the correct order

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Unicode emojis for status
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
GEAR="⚙️"
BRAIN="🧠"
SHIELD="🛡️"
WRENCH="🔧"

echo -e "${PURPLE}${ROCKET} LinkOps MLOps Platform Startup${NC}"
echo -e "${PURPLE}======================================${NC}"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}${GEAR} Creating .env file from template...${NC}"
    cp env.template .env
    echo -e "${GREEN}${CHECK} Created .env file. Please review and update the values.${NC}"
    echo ""
fi

# Function to check service health
check_service_health() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    echo -ne "${YELLOW}${GEAR} Waiting for $service_name to be healthy..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$port/health > /dev/null 2>&1; then
            echo -e "\r${GREEN}${CHECK} $service_name is healthy!                    ${NC}"
            return 0
        fi
        
        echo -ne "\r${YELLOW}${GEAR} Waiting for $service_name to be healthy... ($attempt/$max_attempts)${NC}"
        sleep 2
        ((attempt++))
    done
    
    echo -e "\r${RED}${CROSS} $service_name failed to start properly           ${NC}"
    return 1
}

# Check prerequisites
echo -e "${BLUE}${GEAR} Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}${CROSS} Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}${CROSS} Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}${CHECK} Prerequisites satisfied${NC}"
echo ""

# Stop any existing containers
echo -e "${YELLOW}${GEAR} Stopping any existing containers...${NC}"
docker-compose down --remove-orphans > /dev/null 2>&1 || true
echo -e "${GREEN}${CHECK} Cleaned up existing containers${NC}"
echo ""

# Start infrastructure services first
echo -e "${BLUE}${GEAR} Starting infrastructure services...${NC}"
docker-compose up -d db redis zookeeper kafka
echo ""

# Wait for infrastructure to be ready
echo -e "${YELLOW}${GEAR} Waiting for infrastructure services...${NC}"
sleep 10

# Check infrastructure health
echo -e "${BLUE}${GEAR} Checking infrastructure health...${NC}"

# Check PostgreSQL
if docker-compose exec -T db pg_isready -U linkops > /dev/null 2>&1; then
    echo -e "${GREEN}${CHECK} PostgreSQL is ready${NC}"
else
    echo -e "${RED}${CROSS} PostgreSQL is not ready${NC}"
    exit 1
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}${CHECK} Redis is ready${NC}"
else
    echo -e "${RED}${CROSS} Redis is not ready${NC}"
    exit 1
fi

echo ""

# Start MLOps Platform (main service)
echo -e "${PURPLE}${BRAIN} Starting MLOps Platform...${NC}"
docker-compose up -d mlops_platform
check_service_health "MLOps Platform" 8000
echo ""

# Start MLOps Services
echo -e "${CYAN}${BRAIN} Starting MLOps Services...${NC}"
docker-compose up -d whis_data_input whis_sanitize whis_smithing whis_enhance whis_logic whis_webscraper audit_assess audit_migrate mlops_utils

echo -e "${YELLOW}${GEAR} Checking MLOps service health...${NC}"
check_service_health "Whis Data Input" 8001
check_service_health "Whis Sanitize" 8002
check_service_health "Whis Smithing" 8003
check_service_health "Whis Enhance" 8004
check_service_health "Whis Logic" 8005
check_service_health "Whis Webscraper" 8006
check_service_health "Audit Assess" 8007
check_service_health "Audit Migrate" 8008
check_service_health "MLOps Utils" 8009
echo ""

# Start Shadow Agents
echo -e "${SHIELD}${BRAIN} Starting Shadow Agents...${NC}"
docker-compose up -d jimmie_logic ficknury_evaluator audit_logic auditguard_logic kubernetes_specialist ml_data_scientist platform_engineer devops_engineer

echo -e "${YELLOW}${GEAR} Checking Shadow Agent health...${NC}"
check_service_health "Jimmie Logic" 8010
check_service_health "Ficknury Evaluator" 8011
check_service_health "Audit Logic" 8012
check_service_health "AuditGuard Logic" 8013
check_service_health "Kubernetes Specialist" 8014
check_service_health "ML Data Scientist" 8015
check_service_health "Platform Engineer" 8016
check_service_health "DevOps Engineer" 8017
echo ""

# Start Frontend
echo -e "${BLUE}${WRENCH} Starting Frontend...${NC}"
docker-compose up -d frontend

echo -e "${YELLOW}${GEAR} Waiting for frontend to build and start...${NC}"
sleep 30

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}${CHECK} Frontend is ready!${NC}"
else
    echo -e "${YELLOW}${GEAR} Frontend is still building (this may take a few minutes)${NC}"
fi

echo ""
echo -e "${GREEN}${ROCKET} LinkOps MLOps Platform Started Successfully!${NC}"
echo -e "${GREEN}====================================={}============${NC}"
echo ""
echo -e "${CYAN}📍 Available Services:${NC}"
echo -e "   ${BLUE}Frontend:${NC}              http://localhost:3000"
echo -e "   ${BLUE}MLOps Platform:${NC}        http://localhost:8000"
echo -e "   ${BLUE}Whis Data Input:${NC}       http://localhost:8001"
echo -e "   ${BLUE}Whis Sanitize:${NC}         http://localhost:8002"
echo -e "   ${BLUE}Whis Smithing:${NC}         http://localhost:8003"
echo -e "   ${BLUE}Whis Enhance:${NC}          http://localhost:8004"
echo -e "   ${BLUE}Whis Logic:${NC}            http://localhost:8005"
echo -e "   ${BLUE}Whis Webscraper:${NC}       http://localhost:8006"
echo -e "   ${BLUE}Audit Assess:${NC}          http://localhost:8007"
echo -e "   ${BLUE}Audit Migrate:${NC}         http://localhost:8008"
echo -e "   ${BLUE}MLOps Utils:${NC}           http://localhost:8009"
echo ""
echo -e "${SHIELD}Shadow Agents:${NC}"
echo -e "   ${PURPLE}Jimmie Logic:${NC}          http://localhost:8010"
echo -e "   ${PURPLE}Ficknury Evaluator:${NC}    http://localhost:8011"
echo -e "   ${PURPLE}Audit Logic:${NC}           http://localhost:8012"
echo -e "   ${PURPLE}AuditGuard Logic:${NC}      http://localhost:8013"
echo -e "   ${PURPLE}Kubernetes Specialist:${NC} http://localhost:8014"
echo -e "   ${PURPLE}ML Data Scientist:${NC}     http://localhost:8015"
echo -e "   ${PURPLE}Platform Engineer:${NC}     http://localhost:8016"
echo -e "   ${PURPLE}DevOps Engineer:${NC}       http://localhost:8017"
echo ""
echo -e "${YELLOW}Infrastructure:${NC}"
echo -e "   ${CYAN}PostgreSQL:${NC}            localhost:5432"
echo -e "   ${CYAN}Redis:${NC}                 localhost:6379"
echo -e "   ${CYAN}Kafka:${NC}                 localhost:9092"
echo ""
echo -e "${GREEN}🎉 All services are now running!${NC}"
echo ""
echo -e "${YELLOW}💡 Useful Commands:${NC}"
echo -e "   ${BLUE}View logs:${NC}             docker-compose logs -f [service_name]"
echo -e "   ${BLUE}Stop all services:${NC}     docker-compose down"
echo -e "   ${BLUE}Restart service:${NC}       docker-compose restart [service_name]"
echo -e "   ${BLUE}Check status:${NC}          docker-compose ps"
echo "" 