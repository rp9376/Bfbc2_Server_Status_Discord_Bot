#!/usr/bin/env python3
"""
BFBC2 Server Information Module
Consolidated module for fetching and processing BFBC2 server data.
Provides functions to interact with Project Rome API without using classes.
"""

import os
import requests
import time
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# BFBC2 Map Code to Real Name Mapping
BFBC2_MAP_NAMES = {
    # Base Game Maps
    'Levels/MP_001': 'Panama Canal',
    'Levels/MP_002': 'Valparaiso', 
    'Levels/MP_003': 'Laguna Alta',
    'Levels/MP_004': 'Isla Inocentes',
    'Levels/MP_005': 'Atacama Desert',
    'Levels/MP_006': 'Arica Harbor',
    'Levels/MP_007': 'White Pass',
    'Levels/MP_008': 'Nelson Bay',
    'Levels/MP_009': 'Laguna Presa',
    'Levels/MP_012': 'Port Valdez',
    'Levels/BC1_Oasis': 'Oasis',
    'Levels/BC1_Harvest_Day': 'Harvest Day',
    'Levels/MP_SP_002': 'Cold War',
    'Levels/MP_SP_005': 'Heavy Metal',
    
    # Vietnam DLC Maps
    'Levels/NAM_MP_002': 'Vantage Point',
    'Levels/NAM_MP_003': 'Hill 137',
    'Levels/NAM_MP_005': 'Cao Son Temple',
    'Levels/NAM_MP_006': 'Phu Bai Valley',
    'Levels/NAM_MP_007': 'Operation Hastings',
}

BFBC2_GAME_MODES = {
    "CONQUEST": "Conquest",
    "RUSH": "Rush",
    "SQDM": "Squad Deathmatch",
    "SQRUSH": "Squad Rush",
}

BFBC2_REGIONS = {
    "EU": "Europe",
    "NA": "North America",
    "SA": "South America",
    "AS": "Asia",
    "OC": "Oceania",
    "AF": "Africa",
}


# API Configuration
BASE_URL = "https://fesl.cetteup.com/v1/bfbc2/servers/rome-pc"
DEFAULT_TIMEOUT = 10
DEFAULT_DELAY = 0.02


def get_map_name(level_code):
    """
    Convert a level code to a human-readable map name.
    
    Args:
        level_code (str): The level code from the server (e.g., 'Levels/NAM_MP_005')
        
    Returns:
        str: Human-readable map name or the original code if not found
    """
    return BFBC2_MAP_NAMES.get(level_code, level_code)

def get_game_mode_name(mode_code):
    """
    Convert a game mode code to a human-readable name.
    
    Args:
        mode_code (str): The game mode code from the server (e.g., 'RUSH')
        
    Returns:
        str: Human-readable game mode name or the original code if not found
    """
    return BFBC2_GAME_MODES.get(mode_code, mode_code)

def get_region_name(region_code):
    """
    Convert a region code to a human-readable name.
    
    Args:
        region_code (str): The region code from the server (e.g., 'EU')
        
    Returns:
        str: Human-readable region name or the original code if not found
    """
    return BFBC2_REGIONS.get(region_code, region_code)


def fetch_server_list(timeout=DEFAULT_TIMEOUT):
    """
    Fetch the basic server list from the Project Rome API.
    
    Args:
        timeout (int): Request timeout in seconds
        
    Returns:
        list: List of server dictionaries or empty list on error
    """
    try:
        #print("🔄 Fetching server list from Project Rome API...")
        response = requests.get(BASE_URL, timeout=timeout)
        response.raise_for_status()
        servers = response.json()
        #print(f"✅ Successfully retrieved {len(servers)} servers")
        return servers
    except requests.RequestException as e:
        print(f"❌ Error fetching server list: {e}")
        return []


def fetch_server_details(server, timeout=5):
    """
    Fetch detailed information for a specific server including player list.
    
    Args:
        server (dict): Server information containing LID and GID
        timeout (int): Request timeout in seconds
        
    Returns:
        dict: Detailed server information or None on error
    """
    lid = server['LID']
    gid = server['GID']
    
    try:
        detail_url = f"{BASE_URL}/{lid}/{gid}"
        response = requests.get(detail_url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"⚠️  Failed to get details for server {server.get('N', 'Unknown')}: {e}")
        return None


def find_server_by_name(servers, name):    
    """
    Find a server by its name in the list of servers.
    
    Args:
        servers (list): List of server dictionaries
        name (str): Name of the server to find (case-insensitive partial match)
        
    Returns:
        dict: Server dictionary if found, None otherwise
    """    
    for server in servers:
        if name.lower() in server.get('N', '').lower():
            #print(f"🎯 Found server: {server.get('N', 'Unknown')}")
            return server
    print(f"❌ Server '{name}' not found in the server list")
    return None


def get_server_info(server):
    """
    Extract basic server information from server data.
    
    Args:
        server (dict): Server dictionary containing details
        
    Returns:
        dict: Formatted server information
    """
    if not server:
        return None
        
    level_code = server.get('B-U-level', 'Unknown')
    map_name = get_map_name(level_code)
    game_mode = server.get('B-U-gamemode', 'Unknown')
    game_mode = get_game_mode_name(game_mode)
    region = server.get('B-U-region', 'Unknown')
    region = get_region_name(region)


    return {
        'name': server.get('N', 'Unknown'),
        'players': f"{server.get('AP', 0)}/{server.get('MP', 0)}",
        'current_players': server.get('AP', 0),
        'max_players': server.get('MP', 0),
        'game_mode': game_mode,
        'map': map_name,
        'map_code': level_code,
        'region': region,
        'ip': server.get('I', 'Unknown'),
        'port': server.get('P', 'Unknown'),
        'address': f"{server.get('I', 'Unknown')}:{server.get('P', 'Unknown')}"
    }


def get_player_list(server_details):
    """
    Extract and return the player list from detailed server information.
    
    Args:
        server_details (dict): Detailed server information containing player data
        
    Returns:
        list: List of player names sorted alphabetically, or empty list if no players
    """
    if not server_details:
        return []
    
    players = server_details.get('D-Players', [])
    
    if not players:
        return []

    # Extract player names and sort them alphabetically
    player_names = [player.get('name', 'Unknown') for player in players]
    player_names.sort(key=lambda name: name.lower())

    return player_names


def get_server_with_players(server_name):
    """
    Get complete server information including player list for a specific server.
    
    Args:
        server_name (str): Name of the server to find
        
    Returns:
        dict: Complete server information with player list, or None if not found
    """
    # Fetch all servers
    servers = fetch_server_list()
    if not servers:
        return None
    
    # Find the specific server
    server = find_server_by_name(servers, server_name)
    if not server:
        return None
    
    # Get basic server info
    server_info = get_server_info(server)
    if not server_info:
        return None
    
    # Get detailed information including player list
    server_details = fetch_server_details(server)
    player_list = get_player_list(server_details)
    
    # Combine information
    server_info['players_list'] = player_list
    server_info['player_count'] = len(player_list)
    
    # Add additional details if available
    if server_details:
        server_info['auto_balance'] = server_details.get('D-AutoBalance', None)
        server_info['friendly_fire'] = server_details.get('D-FriendlyFire', None)
        server_info['kill_cam'] = server_details.get('D-KillCam', None)
        server_info['minimap'] = server_details.get('D-Minimap', None)
        server_info['banner_url'] = server_details.get('D-BannerUrl', None)
        server_info['server_description'] = server_details.get('D-ServerDescription0', None)
    
    return server_info


def print_server_info(server_info):
    """
    Print detailed information about a server in a formatted way.
    
    Args:
        server_info (dict): Server information dictionary
    """
    if not server_info:
        print("❌ No server information available")
        return
        
    print("=" * 60)
    print(f"🎮 Server: {server_info['name']}")
    
    # Handle both simple server info and detailed server info with player lists
    if 'player_count' in server_info:
        print(f"👥 Players: {server_info['players']} ({server_info['player_count']} online)")
    else:
        print(f"👥 Players: {server_info['players']}")
    
    print(f"🎯 Game Mode: {server_info['game_mode']}")
    print(f"🗺️  Map: {server_info['map']}")
    print(f"🌍 Region: {server_info['region']}")
    print(f"🔗 Address: {server_info['address']}")
    
    if server_info.get('players_list'):
        print(f"\n👥 Online Players ({len(server_info['players_list'])}):")
        for i, player in enumerate(server_info['players_list'], 1):
            print(f"   {i:2}. {player}")
    elif server_info.get('current_players', 0) == 0:
        print("\n👥 No players currently online")
    
    print("=" * 60)


def get_server_stats(servers):
    """
    Generate statistics from a list of servers.
    
    Args:
        servers (list): List of server dictionaries
        
    Returns:
        dict: Statistics about the servers
    """
    if not servers:
        return {}
    
    active_servers = [s for s in servers if s.get('AP', 0) > 0]
    total_players = sum(s.get('AP', 0) for s in servers)
    total_capacity = sum(s.get('MP', 0) for s in servers)
    
    # Game mode distribution
    game_modes = [s.get('B-U-gamemode', 'Unknown') for s in servers]
    mode_counts = Counter(game_modes)
    
    # Region distribution
    regions = [s.get('B-U-region', 'Unknown') for s in servers]
    region_counts = Counter(regions)
    
    return {
        'total_servers': len(servers),
        'active_servers': len(active_servers),
        'total_players': total_players,
        'total_capacity': total_capacity,
        'capacity_percentage': (total_players / total_capacity * 100) if total_capacity > 0 else 0,
        'game_modes': dict(mode_counts),
        'regions': dict(region_counts)
    }


def print_server_stats(stats):
    """
    Print server statistics in a formatted way.
    
    Args:
        stats (dict): Statistics dictionary from get_server_stats
    """
    if not stats:
        print("❌ No statistics available")
        return
    
    print("\n" + "=" * 60)
    print("📊 BFBC2 SERVER STATISTICS")
    print("=" * 60)
    print(f"🎮 Total Servers: {stats['total_servers']}")
    print(f"🟢 Active Servers: {stats['active_servers']} ({stats['active_servers']/stats['total_servers']*100:.1f}%)")
    print(f"👥 Total Players: {stats['total_players']}/{stats['total_capacity']} ({stats['capacity_percentage']:.1f}% capacity)")
    
    print(f"\n📊 Game Mode Distribution:")
    for mode, count in sorted(stats['game_modes'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {mode:15}: {count:2} servers")
    
    print(f"\n🌍 Regional Distribution:")
    for region, count in sorted(stats['regions'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {region:15}: {count:2} servers")


def monitor_server_from_env():
    """
    Monitor the server specified in the .env file.
    
    Returns:
        dict: Server information or None if not found
    """
    server_name = os.getenv('BFBC2_SERVER_NAME')
    if not server_name:
        print("❌ BFBC2_SERVER_NAME not found in .env file")
        return None
    
    #print(f"🔍 Looking for server: {server_name}")
    return get_server_with_players(server_name)


# Example usage functions for when the script is run independently
def example_monitor_single_server():
    """Example: Monitor a single server specified in .env file."""
    print("🚀 Example: Monitoring single server from .env")
    server_info = monitor_server_from_env()
    if server_info:
        print_server_info(server_info)
    else:
        print("❌ Could not retrieve server information")


def example_search_server():
    """Example: Search for a specific server by name."""
    print("🚀 Example: Searching for a specific server")
    servers = fetch_server_list()
    if servers:
        # Search for a server (you can change this name)
        search_name = "vietnam"
        server = find_server_by_name(servers, search_name)
        if server:
            # Use get_server_with_players to get complete info including player list
            server_info = get_server_with_players(search_name)
            if server_info:
                print_server_info(server_info)
            else:
                # Fallback to basic info
                basic_info = get_server_info(server)
                print_server_info(basic_info)


def example_server_overview():
    """Example: Get overview of all servers."""
    print("🚀 Example: Server overview and statistics")
    servers = fetch_server_list()
    if servers:
        stats = get_server_stats(servers)
        print_server_stats(stats)
        
        # Show top 5 most populated servers
        sorted_servers = sorted(servers, key=lambda x: x.get('AP', 0), reverse=True)
        print(f"\n🔥 Top 5 Most Populated Servers:")
        for i, server in enumerate(sorted_servers[:5], 1):
            info = get_server_info(server)
            print(f"   {i}. {info['name']} - {info['players']} players")


def example_simple_server_info():
    """Example: Get simple server information without player list."""
    print("🚀 Example: Simple server information")
    servers = fetch_server_list()
    if servers:
        for i, server in enumerate(servers[::], 1):  # Limit to first 5 servers
            info = get_server_info(server)
            print("=" * 60)
            print(f"{i}. {info['name']}\nPlayers: {info['players']}\nMap: {info['map']}\nRegion: {info['region']}\nGame Mode: {info['game_mode']}\nAddress: {info['address']}")
    else:
        print("❌ No servers found")


def main():
    """Main function demonstrating various features."""
    print("🎮 BFBC2 Server Information Tool")
    print("=" * 50)
    
    print("Running example demonstrations:\n")
    
    print ("Example 1: Monitor server from .env")
    example_monitor_single_server()
    print("\n" + "-" * 50 + "\n")
    
    print("Example 2: Search for specific server")
    example_search_server()
    print("\n" + "-" * 50 + "\n")
    
    print("Example 3: Server overview")
    example_server_overview()

    print("Example 4: Simple server information")
    example_simple_server_info()
    print("\n" + "=" * 50)
    



if __name__ == "__main__":
    # Clear console for better readability
    os.system('clear' if os.name == 'posix' else 'cls')
    main()
