# BFBC2 Discord Bot - Docker Deployment

A lightweight Discord bot that monitors Battlefield Bad Company 2 server status with Docker support.

## 🐳 Docker Features

- **Lightweight**: Based on Python 3.12-slim image
- **Secure**: Runs as non-root user
- **Resource Limited**: 128MB RAM limit, 0.5 CPU limit
- **Auto-restart**: Automatically restarts on failure
- **Health Checks**: Built-in container health monitoring
- **Logging**: Structured logging with rotation

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Discord Bot Token
- Discord Channel ID

## 🚀 Quick Start

### 1. Clone and Configure

```bash
# Navigate to project directory
cd Bfbc2_Server_Status_Discord_Bot

# Copy environment template
cp .env.docker .env

# Edit configuration
nano .env
```

### 2. Configure Environment Variables

Edit `.env` file with your settings:

```env
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
UPDATE_CHANNEL_ID=your_discord_channel_id_here

# BFBC2 Server Configuration
BFBC2_SERVER_NAME=your_server_name_here

# Update interval in seconds (minimum 10)
UPDATE_INTERVAL_SECONDS=60
```

### 3. Deploy with Docker Compose

#### Using Management Scripts:

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh start
```

**Windows:**
```cmd
run.bat start
```

#### Using Docker Compose directly:

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose stop

# Restart
docker-compose restart
```

## 📊 Management Commands

### Script Commands
```bash
./run.sh start    # Build and start the bot
./run.sh stop     # Stop the bot
./run.sh restart  # Restart the bot
./run.sh logs     # Show real-time logs
```

### Docker Compose Commands
```bash
docker-compose up -d          # Start in background
docker-compose down           # Stop and remove containers
docker-compose logs -f        # Follow logs
docker-compose restart        # Restart services
docker-compose pull           # Update images
```

### Container Management
```bash
# View running containers
docker ps

# Enter container shell (debugging)
docker exec -it bfbc2-discord-bot bash

# View resource usage
docker stats bfbc2-discord-bot

# View container health
docker inspect bfbc2-discord-bot | grep -A 5 Health
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DISCORD_TOKEN` | Discord bot token | - | ✅ |
| `UPDATE_CHANNEL_ID` | Discord channel ID | - | ✅ |
| `BFBC2_SERVER_NAME` | BFBC2 server name to monitor | - | ✅ |
| `UPDATE_INTERVAL_SECONDS` | Update frequency (min 10s) | 60 | ❌ |

### Resource Limits

The container is configured with conservative resource limits:

- **Memory**: 128MB limit, 64MB reserved
- **CPU**: 0.5 cores limit, 0.1 cores reserved
- **Logging**: 10MB max per file, 3 files retained

### Customizing Resources

Edit `docker-compose.yml` to adjust limits:

```yaml
deploy:
  resources:
    limits:
      memory: 256M      # Increase memory limit
      cpus: '1.0'       # Increase CPU limit
```

## 📝 Logs and Monitoring

### View Logs
```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Logs since timestamp
docker-compose logs --since="2024-01-01T00:00:00"
```

### Health Monitoring

The container includes health checks that run every 30 seconds:
- Check if Python can import required modules
- Verify bot process is running
- Container will restart automatically if unhealthy

## 🛠 Troubleshooting

### Common Issues

**Bot not starting:**
```bash
# Check logs
docker-compose logs

# Verify environment
docker-compose config

# Rebuild image
docker-compose build --no-cache
```

**Permission issues:**
```bash
# Fix ownership (Linux/macOS)
sudo chown -R $USER:$USER .

# Verify .env file exists
ls -la .env
```

**Network issues:**
```bash
# Check container network
docker network ls

# Test connectivity
docker exec bfbc2-discord-bot ping 8.8.8.8
```

**Resource constraints:**
```bash
# Check resource usage
docker stats bfbc2-discord-bot

# View system resources
docker system df
```

### Debug Mode

To run with more verbose logging:

```bash
# Stop current container
docker-compose down

# Run with debug output
docker-compose up
```

## 🔄 Updates

### Update Bot Code
```bash
# Stop bot
docker-compose down

# Pull latest code (if using git)
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Update Base Image
```bash
# Pull latest Python image
docker pull python:3.12-slim

# Rebuild container
docker-compose build --no-cache

# Restart with new image
docker-compose up -d
```

## 📦 Image Size

The Docker image is optimized for size:
- **Base**: Python 3.12-slim (~45MB)
- **Dependencies**: ~50MB
- **Total**: ~95MB

## 🔒 Security

- Runs as non-root user (`app`)
- Read-only environment file mounting
- No privileged access required
- Minimal system dependencies
- Regular security updates via base image

## 🌟 Production Deployment

For production environments, consider:

1. **Use Docker Swarm or Kubernetes**
2. **Set up log aggregation** (ELK, Fluentd)
3. **Configure monitoring** (Prometheus, Grafana)
4. **Use secrets management** (Docker secrets, Kubernetes secrets)
5. **Set up backup strategies** for configuration

### Example Production Compose

```yaml
version: '3.8'
services:
  bfbc2-bot:
    image: your-registry/bfbc2-bot:latest
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
        max_attempts: 3
    secrets:
      - discord_token
    environment:
      - DISCORD_TOKEN_FILE=/run/secrets/discord_token
```

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify configuration: `docker-compose config`
3. Test connectivity: `docker exec bfbc2-discord-bot ping google.com`
4. Review Discord bot permissions in your server
