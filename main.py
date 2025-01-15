import csv,os,json
from fastapi import FastAPI, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from sqlalchemy.orm import Session
from models import create_db, Armor, SessionLocal
from typing import List
from collections import defaultdict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

create_db() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_csv_to_db(db: Session):
    with open('armor.csv', mode = 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            armor = Armor(
                set_name = row['Set'],
                slot = row['Slot'],

                skill1 = row['Skill 1'],
                skill1_count = row['Skill 1 Count'],
                skill2 = row['Skill 2'],
                skill2_count = row['Skill 2 Count'],

                gem_level_1 = row['Gem Level 1'],
                gem_level_2 = row['Gem Level 2'],
                gem_level_3 = row['Gem Level 3'],
                gem_level_4 = row['Gem Level 4'],
            )
            db.add(armor)
        db.commit()

@app.on_event("startup")
async def startup():
    #Better logic should be implemented that only updates DB if CSV has been updated
    if os.path.exists("test.db"):
        return
    else:
        db = SessionLocal()
        load_csv_to_db(db)
    pass

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
    armor_sets = parse_armor_sets(armor_data)
    #print(armor_sets)

    return templates.TemplateResponse("index.html",{'request':request,'armor_data':armor_sets})