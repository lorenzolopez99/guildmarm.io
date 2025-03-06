import csv,os,json
import logging
from fastapi import FastAPI, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from sqlalchemy.orm import Session
from models import create_db, Armor, Weapon, SessionLocal
from typing import List
from collections import defaultdict

from equipment_update import get_all_armors, get_all_weapons

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#create_db() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_dict_as_csv(d,filename):
    with open(filename, mode='w',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=d[0].keys())
        writer.writeheader()
        writer.writerows(d)

def load_csv_to_db(db: Session):
    #logging.debug("This is an async route")
    if not os.path.exists("armors.csv"):
        armors_dict = get_all_armors()
        save_dict_as_csv(armors_dict,"armors.csv")
    if not os.path.exists("weapons.csv"):
        weapons_dict = get_all_weapons()
        save_dict_as_csv(weapons_dict,"weapons.csv")

    with open('armors.csv', mode = 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            armor = Armor(
                set_name = row["set"],
                name = row["name"],
                slot = row["slot"],

                defense = row["defense"],
                fire_res = row["fire_res"],
                water_res = row["water_res"],
                thunder_res = row["thunder_res"],
                ice_res = row["ice_res"],
                dragon_res = row["dragon_res"],

                level_1_decoration_slots = row["level_1_decoration_slots"],
                level_2_decoration_slots = row["level_2_decoration_slots"],
                level_3_decoration_slots = row["level_3_decoration_slots"],

                skills = row["skills"],
            )
            db.add(armor)
    with open('weapons.csv', mode = 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            weapon = Weapon(
                name = row["name"],
                type = row["type"],

                damage = row["damage"],

                element_buildup = row["element_buildup"],
                element_type = row["element_type"],

                affinity_mod = row["affinity_mod"],
                defense_mod = row["defense_mod"],

                special = row["special"],
                skills = row["skills"],

                level_1_decoration_slots = row["level_1_decoration_slots"],
                level_2_decoration_slots = row["level_2_decoration_slots"],
                level_3_decoration_slots = row["level_3_decoration_slots"],

                sharpness_base_red = row["sharpness_base_red"],
                sharpness_base_orange = row["sharpness_base_orange"],
                sharpness_base_yellow = row["sharpness_base_yellow"],
                sharpness_base_green = row["sharpness_base_green"],
                sharpness_base_blue = row["sharpness_base_blue"],
                sharpness_base_white = row["sharpness_base_white"],
                sharpness_base_purple = row["sharpness_base_purple"],

                sharpness_max_red = row["sharpness_max_red"],
                sharpness_max_orange = row["sharpness_max_orange"],
                sharpness_max_yellow = row["sharpness_max_yellow"],
                sharpness_max_green = row["sharpness_max_green"],
                sharpness_max_blue = row["sharpness_max_blue"],
                sharpness_max_white = row["sharpness_max_white"],
                sharpness_max_purple = row["sharpness_max_purple"],
            )
            db.add(weapon)
    db.commit()

@app.on_event("startup")
async def startup():
    #Better logic should be implemented that only updates DB if CSV has been updated
    if os.path.exists("test.db"):
        return
    else:
        create_db()
        db = SessionLocal()
        load_csv_to_db(db)

def parse_armor_sets(armor_data):
    armor_sets = {}
    armor_list = []
    for piece in armor_data:
        armor_list.append(piece.to_dict())
        #if piece.set_name not in armor_sets:
        #    armor_sets[piece.set_name] = []
        #armor_sets[piece.set_name].append(piece.to_dict())       
    return armor_list
    
@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    armor_data = db.query(Armor).all()
    weapon_data = db.query(Weapon).all()
    #print(armor_data)
    armor_sets = parse_armor_sets(armor_data)
    #print(armor_sets)

    return templates.TemplateResponse("index.html",{'request':request,'armor_data':armor_sets})