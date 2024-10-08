from fastapi import FastAPI, HTTPException
import json
from typing import List
import os

from utils.utilities import build_menu

ROOT_DIR = os.getcwd()

app = FastAPI()

# Load the game reserves data
with open(os.path.join(ROOT_DIR, "data/game_reserves.json"), "r") as f:
    game_reserves = json.load(f)

@app.post("/game-reserves", response_model=dict)
async def get_game_reserves_by_region(data: dict):
    region_name = data.get('region_name')
    reserves = [reserve for reserve in game_reserves if reserve["region"].lower() == region_name.lower()][:5]
    reserves = build_menu(
        body="Please select what game reserve that you are going to visit.",
        button="Game Reserve",
        title="Game reserves",
        rows=reserves
    )
    if not reserves:
        return {"text": "Sorry, your option is not available at the moment please write region name like Arusha, Dodoma etc"}


@app.post("/region", response_model=dict)
async def get_region_by_reserve(data: dict):
    reserve_name = data.get('reserve_name')
    for reserve in game_reserves:
        _reserve_name = reserve_name.lower()
        if reserve["national_park"].lower() == _reserve_name or reserve['national_park'] in reserve_name.lower():
            return {"id": reserve["id"],"region": reserve["region"]}
    raise {"text":"Game reserve not found, you can try "}



