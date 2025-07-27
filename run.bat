@echo off
setlocal

echo 🎮 BFBC2 Discord Bot - Docker Manager
echo =========================================

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo Creating .env from template...
    copy .env.docker .env
    echo ❌ Please edit .env with your configuration before running the bot!
    pause
    exit /b 1
)

REM Check command line argument
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
goto menu

:start
echo 🔨 Building Docker image...
docker-compose build
echo 🚀 Starting BFBC2 Discord Bot...
docker-compose up -d
echo ✅ Bot started successfully!
echo Use 'docker-compose logs -f' to view logs
echo Use 'docker-compose stop' to stop the bot
goto end

:stop
echo 🛑 Stopping BFBC2 Discord Bot...
docker-compose down
echo ✅ Bot stopped successfully!
goto end

:restart
echo 🔄 Restarting BFBC2 Discord Bot...
docker-compose restart
echo ✅ Bot restarted successfully!
goto end

:logs
echo 📋 Showing bot logs...
docker-compose logs -f
goto end

:menu
echo Usage: %0 {start^|stop^|restart^|logs}
echo.
echo Commands:
echo   start   - Build and start the bot
echo   stop    - Stop the bot
echo   restart - Restart the bot
echo   logs    - Show bot logs
echo.
echo Or run docker-compose commands directly:
echo   docker-compose up -d    # Start in background
echo   docker-compose logs -f  # View logs
echo   docker-compose stop     # Stop the bot

:end
pause
