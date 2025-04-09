import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
import os

def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    # http://localhost:8000/welcome/index.html
    app.mount("/static", StaticFiles(directory="www"), name="static")


# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")

# Starting point ...

@app.get("/smarthouse")
def get_smarthouse_info() -> dict[str, int | float]:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return {
        "no_rooms": len(smarthouse.get_rooms()),
        "no_floors": len(smarthouse.get_floors()),
        "registered_devices": len(smarthouse.get_devices()),
        "area": smarthouse.get_area()
    }

@app.get("/smarthouse/floor")
def get_all_floors():
    """
    This endpoint returns an object that provides information
    about the floors of the smarthouse.
    """

    floors = smarthouse.get_floors()

    return [
        {
            "floor_number": floor.get_level().level,
            "floor_area": floor.get_area()
        }
        for floor in floors
    ]

@app.get("/smarthouse/floor/{Level}")
def get_floor(Level: int):
    """
    This endpoint returns an object that provides information
    about the chosen floor of the smarthouse.
    """
    
    floors = smarthouse.get_floors()

    return [
        {
            "floor_number": floor.get_level().level,
            "floor_area": floor.get_area()
        }
        for floor in floors
        if floor.get_level().level == Level
    ]

@app.get("/smarthouse/floor/{Level}/room")
def get_floor(Level: int):
    """
    This endpoint returns an object that provides information
    about the rooms on chosen floor of the smarthouse.
    """
    
    rooms = smarthouse.get_rooms()

    return [
        {
            "name": room.room_name,
            "area": room.area,
            "floor": room.floor.get_level().level
        }
        for room in rooms
        if room.floor.get_level().level == Level
    ]

@app.get("/smarthouse/floor/{Level}/room/{id}")
def get_floor(Level: int, id: int):
    """
    This endpoint returns an object that provides information
    about a specified roomd on the chosen floor of the smarthouse.
    """

    cursor = repo.cursor()
    cursor.execute("SELECT id, floor, area, name FROM rooms WHERE id = ?", (id,))
    room_data = cursor.fetchone()

    if not room_data:
        return {"error": "Room not found"}
    
    room_id, floor_level, area, name = room_data

    if floor_level != Level:
        return {"error": "Room is not on the specified floor"}
    
    return {
        "name": name,
        "area": area,
        "floor": floor_level
    }

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
