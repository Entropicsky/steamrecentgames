import requests
import time
import csv
import json
import os
import tempfile
import time
from requests.exceptions import JSONDecodeError

from dotenv import load_dotenv

# This script uses the Steam Web API take the steamids in the steamids_to_process.json file and get the recently played games for each steamid.
# If getfriends is set to True, it will also get the friends for each steamid and add them to the steamids_to_process.json file.

# Load the .env file
load_dotenv()

# Get the steamkey from the .env file
steamkey = os.getenv('STEAMKEY')


# Set file names
#to_process_file = 'paladinsplayers_to_process.json' # This is the file that contains the steamids to process
#processed_file = 'processed_paladinsplayers.json' # This is the file that contains the steamids that have been processed
#recently_played_file = 'paladins_recently_played.csv' # This is the file that contains the recently played games for the steamids   
to_process_file = 'steamids_to_process.json' # This is the file that contains the steamids to process
processed_file = 'processed_steamids.json' # This is the file that contains the steamids that have been processed
recently_played_file = 'steam_data.csv' # This is the file that contains the recently played games for the steamids   

# Set getfriends to True to get friends and add them to the to_process list. This will allow you to use a "Kevin Bacon" approach to get more SteamIds to process.
getfriends = False

# Set the maximum number of steamids to find recently played data for. 
total_steamids = 100000


def get_recently_played_games(steamkey, steamid, retries=3):
    url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={steamkey}&steamid={steamid}"
    for i in range(retries):
        try:
            response = requests.get(url, timeout=5)  # Set timeout to 5 seconds
            return response.json()
        except (requests.exceptions.Timeout, JSONDecodeError):
            delay = 2  # Wait for 2 seconds
            print(f"Request timed out or failed to decode JSON, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Failed to get response or decode JSON after multiple attempts")


def get_friends(steamkey, steamid):
    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={steamkey}&steamid={steamid}&relationship=friend"
    response = requests.get(url)
    friends_data = response.json()
    num_friends = len(friends_data.get('friendslist', {}).get('friends', []))
    print(f"{num_friends} friends found for SteamId {steamid}")
    return friends_data

def write_to_file(filename, data):
    with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
        json.dump(data, tmp)
    os.replace(tmp.name, filename)

def gather_info(steamkey, total_steamids, getfriends=False):
    try:
        with open(processed_file, 'r') as file:
            processed_steamids = set(json.load(file))
    except FileNotFoundError:
        processed_steamids = set()

    try:
        with open(to_process_file, 'r') as file:
            steamids_to_process = json.load(file)
    except FileNotFoundError:
        steamids_to_process = []

    steamids_processed = len(processed_steamids)

    while steamids_processed < total_steamids and steamids_to_process:
        current_steamid = steamids_to_process.pop(0)
        if current_steamid not in processed_steamids:
            try:
                games = get_recently_played_games(steamkey, current_steamid)
                if 'games' in games['response'] and games['response']['games']:
                    print(f"Processing {current_steamid} with {len(games['response']['games'])} games.")
                    with open(recently_played_file, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        for game in games['response']['games']:
                            if all(key in game for key in ['appid', 'name', 'playtime_2weeks', 'playtime_forever']):
                                writer.writerow([current_steamid, game['appid'], game['name'], game['playtime_2weeks'], game['playtime_forever']])
                            else:
                                print(f"Missing data for game: {game}")
                            file.flush()  # Flush the file buffer after each row
                    # note we only get friends if we found recently played games. Saves on API calls since you aren't likely to get friends if you didn't get recently played games.
                    if getfriends:
                        friends = get_friends(steamkey, current_steamid)
                        if 'friendslist' in friends and 'friends' in friends['friendslist']:
                            for friend in friends['friendslist']['friends']:
                                if friend['steamid'] not in processed_steamids:
                                    steamids_to_process.append(friend['steamid'])                    
                        steamids_processed += 1
                else:
                    print(f"No data for {current_steamid}")
                processed_steamids.add(current_steamid)
            except Exception as e:
                print(f"Error processing {current_steamid}: {e}")
            write_to_file(processed_file, list(processed_steamids))
            write_to_file(to_process_file, steamids_to_process)
        time.sleep(0.125)  # To prevent rate limiting
    print(f"Processed {steamids_processed} steamids.")

    

# SET GETFRIENDS = TRUE TO GET FRIENDS. OTHERWISE, IT
gather_info(steamkey, total_steamids, getfriends)