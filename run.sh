#!/bin/bash

# BFBC2 Discord Bot - Docker Management Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎮 BFBC2 Discord Bot - Docker Manager${NC}"
echo "========================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found!${NC}"
    echo "Creating .env from template..."
    cp .env.docker .env
    echo -e "${RED}❌ Please edit .env with your configuration before running the bot!${NC}"
    exit 1
fi

# Function to build and start the bot
start_bot() {
    echo -e "${GREEN}🔨 Building Docker image...${NC}"
    docker-compose build

    echo -e "${GREEN}🚀 Starting BFBC2 Discord Bot...${NC}"
    docker-compose up -d

    echo -e "${GREEN}✅ Bot started successfully!${NC}"
    echo "Use 'docker-compose logs -f' to view logs"
    echo "Use 'docker-compose stop' to stop the bot"
}

# Function to stop the bot
stop_bot() {
    echo -e "${YELLOW}🛑 Stopping BFBC2 Discord Bot...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Bot stopped successfully!${NC}"
}

# Function to view logs
show_logs() {
    echo -e "${GREEN}📋 Showing bot logs...${NC}"
    docker-compose logs -f
}

# Function to restart the bot
restart_bot() {
    echo -e "${YELLOW}🔄 Restarting BFBC2 Discord Bot...${NC}"
    docker-compose restart
    echo -e "${GREEN}✅ Bot restarted successfully!${NC}"
}

# Main menu
case "${1:-menu}" in
    "start")
        start_bot
        ;;
    "stop")
        stop_bot
        ;;
    "restart")
        restart_bot
        ;;
    "logs")
        show_logs
        ;;
    "menu"|*)
        echo "Usage: $0 {start|stop|restart|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Build and start the bot"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  logs    - Show bot logs"
        echo ""
        echo "Or run docker-compose commands directly:"
        echo "  docker-compose up -d    # Start in background"
        echo "  docker-compose logs -f  # View logs"
        echo "  docker-compose stop     # Stop the bot"
        ;;
esac
