#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#    "duckdb",
#    "tqdm",
# ]
# ///
import os
import sys
import json
import duckdb
from tqdm import tqdm


results = json.load(open("results_aggregated.json"))

# make audio folder
try:
    os.mkdir("audio")
except:
    pass
cwd = os.getcwd()
found_audio = {}
for result in tqdm(results):
    identifier = result["identifier"]
    audio_dir = os.path.join(
        "/media/zns/backup4tb/aporee-forests/download_output", identifier
    )
    # find all ogg files in directory
    for root, dirs, files in os.walk(audio_dir):
        for file in files:
            if file.endswith(".ogg"):
                found_audio[identifier] = True
                full_path = os.path.join(root, file)
                # copy to the audio folder
                os.system(f"cp {full_path} audio/{identifier}.ogg")
                break
        if identifier in found_audio:
            break

# create a duckdb database
# columns: identifier (text), latitude (float), longitude (float),
# description (text), title (text),
# water (bool), forest (bool), birds (bool), city (bool), talking (bool)
database_file = "aporee.duckdb"
con = duckdb.connect(database_file)
con.execute(
    "CREATE OR REPLACE TABLE aporee (identifier TEXT, latitude FLOAT, longitude FLOAT, description TEXT, title TEXT, water BOOLEAN, forest BOOLEAN, birds BOOLEAN, city BOOLEAN, talking BOOLEAN)"
)

for result in tqdm(results):
    if result["identifier"] not in found_audio:
        continue
    water = "water" in result["groupings"]
    forest = "forest" in result["groupings"]
    birds = "birds" in result["groupings"]
    city = "city" in result["groupings"]
    talking = "talking" in result["groupings"]
    con.execute(
        "INSERT INTO aporee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            result["identifier"],
            result["latitude"],
            result["longitude"],
            result["description"],
            result["title"],
            water,
            forest,
            birds,
            city,
            talking,
        ),
    )

con.close()
