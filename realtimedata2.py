from nba_api.stats.endpoints import leaguedashplayerstats # pyright: ignore[reportMissingImports]
import datetime
import pandas as pd
import json
from pymongo import MongoClient


# Example call — adjust parameters as needed
df = leaguedashplayerstats.LeagueDashPlayerStats(
    per_mode_detailed='Totals',
    season_type_all_star='Regular Season',
).get_data_frames()[0]

df.drop(df.columns[1], axis=1)
date_time = datetime.datetime.now()
json_file = f"nba_player_totals_{date_time}.json"
df.to_excel(f"nba_player_totals_{date_time}.xlsx", index=False)
json_string = df.to_json(orient='records', indent=4)
with open(json_file, 'w') as f:
        f.write(json_string)

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
