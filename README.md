# 🎮 BFBC2 Discord Server Monitor Bot

A Discord bot that monitors Battlefield: Bad Company 2 server status in real-time, providing live updates on player counts, maps, game modes, and online players. Built with love, caffeine, and a generous amount of agentic coding! ✨

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.5.2-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🚀 **Real-time server monitoring** with customizable update intervals
- 👥 **Live player tracking** showing all online players in organized columns
- 🗺️ **Map and game mode information** with proper BFBC2 map name translations
- 📊 **Beautiful Discord embeds** with emojis and color-coded status indicators
- ⚙️ **Configurable via environment variables** - no code changes needed
- 🐳 **Docker support** for easy deployment and lightweight containers
- 🧹 **Graceful shutdown** with automatic cleanup of Discord messages
- 🔄 **Auto-recovery** from network issues and API errors
- 🎯 **Single server focus** - monitor exactly what you need

## 📸 Screenshots

The bot creates dynamic embeds showing:
- Server name and status (🟢 Active / 🟡 Empty / 🔴 Offline)
- Current map and game mode
- Player count with full player list in two columns
- Real-time updates with configurable intervals

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bfbc2-discord-bot.git
   cd bfbc2-discord-bot
   ```

2. **Create your environment file**
   ```bash
   cp env.example .env
   ```

3. **Configure your settings** (edit `.env`):
   ```env
   DISCORD_TOKEN=your_bot_token_here
   UPDATE_CHANNEL_ID=your_channel_id_here
   BFBC2_SERVER_NAME=Your Server Name
   UPDATE_INTERVAL_SECONDS=30
   ```

4. **Run with Docker**
   ```bash
   docker-compose up -d
   ```

### Option 2: Local Python

1. **Install Python 3.8+** and clone the repository

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (copy and edit `.env` from `env.example`)

4. **Run the bot**
   ```bash
   python bfbc2_discord_bot.py
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DISCORD_TOKEN` | Your Discord bot token | - | ✅ Yes |
| `UPDATE_CHANNEL_ID` | Discord channel ID for updates | - | ⚠️ Optional* |
| `BFBC2_SERVER_NAME` | BFBC2 server name to monitor | - | ✅ Yes |
| `UPDATE_INTERVAL_SECONDS` | Update frequency (min: 10s) | 120 | ❌ No |

*\*Can be set via the `!setchannel` command in Discord*

### Getting Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section
4. Create a bot and copy the token
5. Enable "Message Content Intent" under "Privileged Gateway Intents"

### Getting Channel ID

1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click on your desired channel
3. Select "Copy ID"

## 🤖 Bot Commands

| Command | Permission | Description |
|---------|------------|-------------|
| `!info` | Everyone | Show bot information and features |
| `!server` | Everyone | Get current server status on-demand |
| `!setchannel` | Admin | Set the current channel for updates |
| `!refresh` | Admin | Force refresh the server status |

## 🐳 Docker Deployment

### Simple Deployment
```bash
# Clone and configure
git clone <your-repo>
cd bfbc2-discord-bot
cp env.example .env
# Edit .env with your settings

# Deploy
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production Deployment

The Docker setup includes:
- 🏋️ **Lightweight**: Python 3.12-slim base image
- 🔒 **Secure**: Non-root user execution
- 📊 **Resource limits**: Memory and CPU constraints
- 🔄 **Auto-restart**: Container restarts on failures
- 📁 **Volume mounting**: Easy configuration updates

## 🏗️ Architecture

### Project Structure
```
bfbc2-discord-bot/
├── 🐍 bfbc2_discord_bot.py    # Main Discord bot logic
├── 🌐 bfbc2_server.py         # BFBC2 server API functions
├── 📋 requirements.txt        # Python dependencies
├── 🐳 Dockerfile             # Container image definition
├── 🐙 docker-compose.yml     # Multi-container orchestration
├── ⚙️ .env.example           # Configuration template
├── 🚀 run.sh / run.bat       # Platform-specific runners
└── 📚 README.md              # This amazing documentation!
```

### Core Modules

**`bfbc2_discord_bot.py`** - The heart of the operation
- Discord bot setup and event handling
- Real-time server monitoring with background tasks
- Command processing and embed generation
- Graceful shutdown with message cleanup
- Signal handling for container deployments

**`bfbc2_server.py`** - The data powerhouse
- Project Rome API integration
- BFBC2 map name translations (50+ maps supported)
- Server search and player list parsing
- Game mode detection and formatting
- Error handling and retry logic

## 📊 Monitoring & Logging

The bot provides comprehensive logging:
- ✅ Connection status and guild information
- 🔄 Server update cycles and state changes
- ❌ Error handling with detailed messages
- 🧹 Cleanup operations and graceful shutdowns

Example logs:
```
Discord.py imported successfully!
bfbc2-discord-bot    | 🎮 Starting BFBC2 Discord Bot...
bfbc2-discord-bot    | Bot connected to Discord!
bfbc2-discord-bot    | Monitoring server: [Your Server Name]
bfbc2-discord-bot    | Update interval: 30 seconds
bfbc2-discord-bot    | Sent new server status message
```

## 🔧 Troubleshooting

### Common Issues

**Bot doesn't respond to commands**
- ✅ Check if bot has "Message Content Intent" enabled
- ✅ Verify bot has appropriate permissions in your server
- ✅ Ensure the bot token is correct in `.env`

**Server not found**
- ✅ Check `BFBC2_SERVER_NAME` matches exactly (partial matching supported)
- ✅ Verify the server is online and visible on Project Rome
- ✅ Try using a shorter, unique part of the server name

**Updates not appearing**
- ✅ Set channel with `!setchannel` command or configure `UPDATE_CHANNEL_ID`
- ✅ Check bot has "Send Messages" and "Embed Links" permissions
- ✅ Verify update interval isn't too short (minimum 10 seconds)

**Docker container issues**
- ✅ Check logs: `docker-compose logs bfbc2-bot`
- ✅ Verify `.env` file exists and is properly configured
- ✅ Ensure Discord token doesn't have extra spaces/characters

## 🎯 Advanced Features

### Custom Update Intervals
```env
# Ultra-fast updates (for active monitoring)
UPDATE_INTERVAL_SECONDS=10

# Standard updates (balanced)
UPDATE_INTERVAL_SECONDS=30

# Relaxed updates (low traffic)
UPDATE_INTERVAL_SECONDS=300
```

### Server Name Matching
The bot supports partial matching, so you can use:
```env
# Full name
BFBC2_SERVER_NAME=My Awesome BFBC2 Server [24/7]

# Partial name (easier)
BFBC2_SERVER_NAME=My Awesome

# Even shorter
BFBC2_SERVER_NAME=Awesome
```

## 🔮 Future Enhancements

- 📈 Player count history and statistics
- 📱 Mobile-friendly embed layouts
- 🎯 Multi-server monitoring support
- 📊 Advanced analytics and graphs
- 🔔 Custom notification triggers
- 🎨 Customizable embed themes

## 🤝 Contributing

This project was gloriously vibe-coded with a perfect blend of:
- ☕ **Caffeine-fueled creativity**
- 🤖 **Agentic coding assistance** 
- ❤️ **Pure passion for BFBC2**
- 🎯 **Community-driven features**

Want to contribute? We'd love your help! Whether it's:
- 🐛 Bug fixes and improvements
- ✨ New features and enhancements
- 📚 Documentation improvements
- 🎨 UI/UX suggestions

Just fork, code, and submit a PR! Let's keep the BFBC2 community alive together! 🎮

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🎖️ **Project Rome** for providing the BFBC2 server API
- 🤖 **Discord.py** team for the amazing library
- 🌟 **BFBC2 Community** for keeping this legendary game alive
- 🤝 **AI Coding Assistants** for the collaborative development experience

## 📞 Support

Having issues? Need help? Want to share your awesome server?

- 📁 **GitHub Issues**: Report bugs and request features
- 💬 **Discord**: Join the BFBC2 community discussions
- 📧 **Email**: Reach out for direct support

---

*Made with ❤️ for the BFBC2 community. Keep the battlefield alive!* 🎮⚔️

**"In a world full of modern shooters, be a Bad Company 2 legend."** ✨
