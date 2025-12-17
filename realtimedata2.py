from nba_api.stats.endpoints import leaguedashplayerstats # pyright: ignore[reportMissingImports]
from nba_api.stats.endpoints  import shotchartdetail
from nba_api.stats.static import players
import datetime
import pandas as pd
import json
from pymongo import MongoClient
import matplotlib.pyplot as plt
from mplbasketball import Court
import random


# Example call — adjust parameters as needed
df = leaguedashplayerstats.LeagueDashPlayerStats(
    per_mode_detailed='Totals',
    season_type_all_star='Regular Season',
).get_data_frames()[0]

df.drop(df.columns[1], axis=1)
date_time = datetime.datetime.now()
json_file = f"nba_player_totals_{date_time}.json"
exceldoc = df.to_excel(f"nba_player_totals_{date_time}.xlsx", index=False)
json_string = df.to_json(orient='records', indent=4)
with open(json_file, 'w') as f:
        f.write(json_string)

#for i in range(len(exceldoc[0]))
readexcel = pd.read_excel(f"nba_player_totals_{date_time}.xlsx")
playeridlist = readexcel['PLAYER_ID'].to_list()

# Create a MongoClient object
client = MongoClient('mongodb://localhost:27017/')

# Access a specific database (it is created automatically when you first add data)
# Replace 'my_database_name' with your desired database name
db = client['nosql_nba_data']

# Access a collection (equivalent to a table in SQL)
# Replace 'my_collection_name' with your desired collection name
collection = db['player_data']

with open(json_file) as f:
    # json.load() converts the JSON data into a Python dictionary or list
    file_data = json.load(f)

# 3. Insert data into the collection
if isinstance(file_data, list):
    # Use insert_many() for a JSON array (list of documents)
    collection.insert_many(file_data)
    print(f"Inserted {len(file_data)} documents.")
else:
    # Use insert_one() for a single JSON object (one document)
    collection.insert_one(file_data)
    print("Inserted 1 document.")
client.close()

court = Court(court_type="nba", origin="center")
fig, ax = plt.subplots(figsize=(6, 5))

random_player = players.find_player_by_id(random.choice(playeridlist))
print(random_player)
#random_player_id = random_player['id']
team_id = 0

shot_json = shotchartdetail.ShotChartDetail(
     team_id=team_id,
     player_id=random_player['id'],
     context_measure_simple='FGA',
     season_nullable='2024-25',
     season_type_all_star='Regular Season'
)

shot_df = shot_json.get_data_frames()[0]
print(f"Fetched {len(shot_df)} shots for {random_player['full_name']}.")
# Display the first few rows of the data frame
print(shot_df[['LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG', 'SHOT_TYPE', 'SHOT_ZONE_BASIC']].head())

# Filtering data for makes and misses
makes = shot_df[shot_df['SHOT_MADE_FLAG'] == 1]
misses = shot_df[shot_df['SHOT_MADE_FLAG'] == 0]

plt.figure(figsize=(12, 11))
plt.scatter(misses['LOC_X'], misses['LOC_Y'], color='red', marker='x', label='Miss')
plt.scatter(makes['LOC_X'], makes['LOC_Y'], color='green', marker='o', label='Make', alpha=0.6)
plt.title(f"{random_player['full_name']} Shot Chart (Makes vs Misses)")
plt.legend()
plt.xlim(-300, 300)
plt.ylim(-100, 500)
#plt.show()


court.draw(ax=ax)
plt.show()

