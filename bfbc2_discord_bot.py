import asyncio
import os
import datetime
import signal
import sys
from dotenv import load_dotenv
from bfbc2_server import monitor_server_from_env, get_server_with_players

# Try to import discord with error handling
try:
    import discord
    from discord.ext import commands, tasks
    print("Discord.py imported successfully!")
except ImportError as e:
    print(f"Error importing discord: {e}")
    exit(1)

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True

# Create bot without voice support
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Channel ID where the bot will post updates
UPDATE_CHANNEL_ID = os.getenv('UPDATE_CHANNEL_ID')
if UPDATE_CHANNEL_ID and UPDATE_CHANNEL_ID.strip():
    try:
        UPDATE_CHANNEL_ID = int(UPDATE_CHANNEL_ID)
    except ValueError:
        UPDATE_CHANNEL_ID = None
else:
    UPDATE_CHANNEL_ID = None

# BFBC2 Server name to monitor
BFBC2_SERVER_NAME = os.getenv('BFBC2_SERVER_NAME')

# Update interval in seconds (default: 120 seconds = 2 minutes)
UPDATE_INTERVAL_SECONDS = os.getenv('UPDATE_INTERVAL_SECONDS')
if UPDATE_INTERVAL_SECONDS:
    try:
        UPDATE_INTERVAL_SECONDS = int(UPDATE_INTERVAL_SECONDS)
        # Minimum 10 seconds to avoid API rate limits
        if UPDATE_INTERVAL_SECONDS < 10:
            print("Warning: Update interval too low, setting to minimum 10 seconds")
            UPDATE_INTERVAL_SECONDS = 10
    except ValueError:
        print("Warning: Invalid UPDATE_INTERVAL_SECONDS, using default 120 seconds")
        UPDATE_INTERVAL_SECONDS = 120
else:
    UPDATE_INTERVAL_SECONDS = 120

# Global variables to track the message and server state
current_message = None
last_server_state = None
shutdown_event = None

def format_player_columns(players):
    """Split player list into two columns for separate fields"""
    if not players:
        return None, None
    
    # Split players into two columns
    mid_point = (len(players) + 1) // 2
    column1 = players[:mid_point]
    column2 = players[mid_point:]
    
    # Format each column
    column1_text = '\n'.join([f"• {player}" for player in column1])
    column2_text = '\n'.join([f"• {player}" for player in column2]) if column2 else "‌"  # invisible character if empty
    
    return column1_text, column2_text

@bot.event
async def on_ready():
    global shutdown_event
    
    # Initialize shutdown event
    shutdown_event = asyncio.Event()
    
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    print(f'Monitoring server: {BFBC2_SERVER_NAME}')
    print(f'Update interval: {UPDATE_INTERVAL_SECONDS} seconds')
    
    # Start the background task with dynamic interval
    send_server_updates.change_interval(seconds=UPDATE_INTERVAL_SECONDS)
    send_server_updates.start()
    
    # Start the shutdown monitor task
    shutdown_monitor.start()

@tasks.loop()
async def shutdown_monitor():
    """Monitor for shutdown signal and cleanup when needed"""
    await shutdown_event.wait()
    
    # Shutdown event was set - perform cleanup
    await cleanup_and_exit()

@tasks.loop()  # Will be set dynamically
async def send_server_updates():
    """Send or update BFBC2 server status message"""
    global current_message, last_server_state
    
    if UPDATE_CHANNEL_ID is None:
        print("No channel ID set - waiting for !setchannel command")
        return
    
    if not BFBC2_SERVER_NAME:
        print("No BFBC2 server name configured in .env")
        return
    
    channel = bot.get_channel(UPDATE_CHANNEL_ID)
    if not channel:
        print(f"Channel {UPDATE_CHANNEL_ID} not found")
        return
    
    try:
        # Get server information
        server_info = monitor_server_from_env()
        
        if not server_info:
            # Server not found or API error
            embed = discord.Embed(
                title="❌ Server Offline",
                description=f"Could not find server: **{BFBC2_SERVER_NAME}**",
                color=0xff0000,
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name="Status", value="🔴 Offline/Not Found", inline=True)
            embed.set_footer(text="BFBC2 Server Monitor")
        else:
            # Server found - create status embed
            is_empty = server_info['current_players'] == 0
            color = 0x00ff00 if server_info['current_players'] > 0 else 0xffaa00 if not is_empty else 0xff6600
            
            embed = discord.Embed(
                title=f"{server_info['name']}",
                #description=f"**{server_info['map']}** - {server_info['game_mode']}",
                color=color,
                timestamp=datetime.datetime.now()
            )
            
            # Player information
            player_status = "🟢 Active" if server_info['current_players'] > 0 else "🟡 Empty"
            embed.add_field(name="🗺️ Map", value=f"{server_info['map']}", inline=True)
            embed.add_field(name="🎯 Game Mode", value=server_info['game_mode'], inline=True)
            embed.add_field(name="📊 Status", value=player_status, inline=True)
            
            # Show online players if any
            player_list = server_info['players_list']
            
            if player_list:
                column1_text, column2_text = format_player_columns(player_list)
                
                # Add player count header
                embed.add_field(
                    name=f"👥 Online Players: {server_info['players']}", 
                    value="", 
                    inline=False
                )
                
                # Add two separate columns as inline fields
                embed.add_field(name="", value=column1_text, inline=True)
                embed.add_field(name="", value=column2_text, inline=True)
                
                # Add empty field to break the line for better layout
                embed.add_field(name="", value="", inline=True)
        
            #embed.add_field(name="🔗 Server Address", value=f"`{server_info['address']}`", inline=False)
            
            # Dynamic footer text based on update interval
            if UPDATE_INTERVAL_SECONDS >= 60:
                interval_text = f"{UPDATE_INTERVAL_SECONDS // 60} minute{'s' if UPDATE_INTERVAL_SECONDS // 60 != 1 else ''}"
            else:
                interval_text = f"{UPDATE_INTERVAL_SECONDS} second{'s' if UPDATE_INTERVAL_SECONDS != 1 else ''}"
            embed.set_footer(text=f"Updates every {interval_text} • BFBC2 Server Monitor")
        
        # Check if server state changed significantly
        state_changed = (
            last_server_state is None or
            (server_info is None) != (last_server_state is None) or
            (server_info and last_server_state and 
             (server_info['current_players'] != last_server_state.get('current_players') or
              server_info['map'] != last_server_state.get('map')))
        )
        
        # Update last server state
        last_server_state = server_info.copy() if server_info else None
        
        # If we don't have a current message or it was deleted, send a new one
        if current_message is None:
            current_message = await channel.send(embed=embed)
            print(f"Sent new server status message")
        else:
            try:
                # Try to edit the existing message
                await current_message.edit(embed=embed)
                status = "with changes" if state_changed else "routine update"
                #print(f"Updated server status message ({status})")
            except discord.NotFound:
                # Message was deleted, send a new one
                current_message = await channel.send(embed=embed)
                print(f"Message was deleted, sent new server status message")
            except discord.HTTPException as e:
                # Some other error, try to send a new message
                print(f"HTTP error: {e}")
                current_message = await channel.send(embed=embed)
                
    except Exception as e:
        print(f"Error updating server status: {e}")
        # Reset current_message on error so we can try again
        current_message = None


# Store bot start time
@bot.event
async def on_connect():
    bot.start_time = datetime.datetime.now()
    print("Bot connected to Discord!")

async def cleanup_and_exit():
    """Clean up resources before exiting"""
    global current_message
    
    print("🧹 Cleaning up...")
    
    # Delete the status message if it exists
    if current_message:
        try:
            await current_message.delete()
            print("✅ Status message deleted from Discord")
        except discord.NotFound:
            print("ℹ️ Status message was already deleted")
        except discord.HTTPException as e:
            print(f"⚠️ Could not delete status message: {e}")
        except Exception as e:
            print(f"❌ Error deleting message: {e}")
    
    # Stop the background task
    if send_server_updates.is_running():
        send_server_updates.cancel()
        print("✅ Background task stopped")
    
    # Close the bot connection
    if not bot.is_closed():
        await bot.close()
        print("✅ Bot connection closed")
    
    print("👋 Goodbye!")
    # Exit the program
    os._exit(0)

def signal_handler(sig, frame):
    """Handle Ctrl+C and other termination signals"""
    print(f"\n📡 Received signal {sig}")
    print("🧹 Initiating cleanup...")
    
    # Set the shutdown event to trigger cleanup
    if shutdown_event:
        shutdown_event.set()
    else:
        # If bot hasn't started yet, just exit
        print("👋 Goodbye!")
        sys.exit(0)

# Run the bot
if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please add your bot token to the .env file")
    else:
        print("Starting bot...")
        print("Press Ctrl+C to stop the bot and clean up...")
        try:
            bot.run(token)
        except KeyboardInterrupt:
            print("\n📡 Keyboard interrupt received")
            # Signal handler will take care of cleanup
        except Exception as e:
            print(f"Error running bot: {e}")
            # Try to cleanup even on error
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(cleanup_and_exit())
                loop.close()
            except Exception as cleanup_error:
                print(f"❌ Error during cleanup: {cleanup_error}")
            finally:
                print("👋 Goodbye!")
                sys.exit(1)
