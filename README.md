# Steam Data Collector

This Python script, `main.py`, is designed to interact with the Steam Web API to gather data about users' recently played games. It can also fetch the friends list of each user if the `getfriends` flag is set to `True`. This script is useful for data analysis, game recommendation systems, or any other application where you need to analyze Steam user behavior.

## Features

- Fetches recently played games for a list of Steam IDs.
- Optionally fetches friends list for each Steam ID.
- Handles API request failures and JSON decoding errors.
- Prevents rate limiting by adding a delay between requests.
- Writes data to CSV and JSON files.

## Requirements

- Python 3.6+
- `requests` library
- `python-dotenv` library

## Setup

1. Clone this repository.

2. Install the required Python libraries using pip:
pip install requests python-dotenv

3. Create a `.env` file in the same directory as `main.py` and add your Steam API key (obtain a key at https://steamcommunity.com/dev):
STEAMKEY=your_steam_api_key


## Usage

You can run the script using the following command:
python main.py


By default, the script will not fetch the friends list for each Steam ID and add those steamids to the list to be processed ("Kevin Bacon" algorithm). If you want to enable this feature, set the `getfriends` variable to `True` in `main.py`.

## Configuration

You can configure the script by modifying the following variables in `main.py`:

- `to_process_file`: The JSON file that contains the Steam IDs to process. REQUIRED TO EXIST WHEN YOU RUN THE SCRIPT.
For example: ["76561199071987314", "76561199072012698", "76561199072123582", "76561199072181907"]

- `processed_file`: The name of the JSON file that contains the Steam IDs that have already been processed. THE SCRIPT WILL CREATE THIS FILE IF IT DOESN'T EXIST, YOU JUST HAVE TO NAME IT. This allows the script to be stopped and started and pick up where it left off. 

- `recently_played_file`: The CSV file that contains the recently played games for the Steam IDs. THIS IS THE NAME OF YOUR RESULTS FILE. THE SCRIPT WILL CREATE IT IF IT DOESN'T EXIST ALREADY. 

- `getfriends`: Whether to fetch the friends list for each Steam ID and those IDS to the to_process_file. 

- `total_steamids`: The maximum number of Steam IDs to process.

- `time_to_sleep`: The time to sleep between requests to prevent rate limiting (in seconds)



## License

This project is licensed under the MIT License.