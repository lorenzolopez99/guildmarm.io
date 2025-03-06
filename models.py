from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Armor(Base):
    __tablename__ = "armor"
    
    id = Column(Integer, primary_key=True,index=True)
    set_name = Column(String)
    name = Column(String)
    slot = Column(String)

    defense = Column(Integer)
    fire_res = Column(Integer)
    water_res = Column(Integer)
    thunder_res = Column(Integer)
    ice_res = Column(Integer)
    dragon_res = Column(Integer)

    level_1_decoration_slots = Column(Integer)
    level_2_decoration_slots = Column(Integer)
    level_3_decoration_slots = Column(Integer)

    skills = Column(String)
    #materials?
    #LR v HR?
    def to_dict(self):
        return {
            "id":self.id,
            "set_name":self.set_name,
            "name":self.name,
            "slot":self.slot,

            "defense":self.defense,
            "fire_res":self.fire_res,
            "water_res":self.water_res,
            "thunder_res":self.thunder_res,
            "ice_res":self.ice_res,
            "dragon_res":self.dragon_res,

            "level_1_decoration":self.level_1_decoration_slots,
            "level_2_decoration":self.level_2_decoration_slots,
            "level_3_decoration":self.level_3_decoration_slots,

            "skills":self.skills
        }

class Weapon(Base):
    __tablename__ = "weapon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)

    damage = Column(Integer)

    element_buildup = Column(Integer)
    element_type = Column(String)

    affinity_mod = Column(Integer)
    defense_mod = Column(Integer)

    special = Column(String)
    skills = Column(String)

    level_1_decoration_slots = Column(Integer)
    level_2_decoration_slots = Column(Integer)
    level_3_decoration_slots = Column(Integer)

    sharpness_base_red = Column(Integer)
    sharpness_base_orange = Column(Integer)
    sharpness_base_yellow = Column(Integer)
    sharpness_base_green = Column(Integer)
    sharpness_base_blue = Column(Integer)
    sharpness_base_white = Column(Integer)
    sharpness_base_purple = Column(Integer)

    sharpness_max_red = Column(Integer)
    sharpness_max_orange = Column(Integer)
    sharpness_max_yellow = Column(Integer)
    sharpness_max_green = Column(Integer)
    sharpness_max_blue = Column(Integer)
    sharpness_max_white = Column(Integer)
    sharpness_max_purple = Column(Integer)
    #Rarity?
    #materials?

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "type": self.type,

            "damage":self.damage,

            "element_buildup":self.element_buildup,
            "element_type":self.element_type,

            "affinity_mod":self.affinity_mod,
            "defense_mod":self.defense_mod,

            "special":self.special,
            "skills":self.skills,

            "level_1_decoration_slots": self.level_1_decoration_slots,
            "level_2_decoration_slots": self.level_2_decoration_slots,
            "level_3_decoration_slots": self.level_3_decoration_slots,

            "sharpness_base_red": self.sharpness_base_red,
            "sharpness_base_orange": self.sharpness_base_orange,
            "sharpness_base_yellow": self.sharpness_base_yellow,
            "sharpness_base_green": self.sharpness_base_green,
            "sharpness_base_blue": self.sharpness_base_blue,
            "sharpness_base_white": self.sharpness_base_white,
            "sharpness_base_purple": self.sharpness_base_purple,

            "sharpness_max_red": self.sharpness_max_red,
            "sharpness_max_orange": self.sharpness_max_orange,
            "sharpness_max_yellow": self.sharpness_max_yellow,
            "sharpness_max_green": self.sharpness_max_green,
            "sharpness_max_blue": self.sharpness_max_blue,
            "sharpness_max_white": self.sharpness_max_white,
            "sharpness_max_purple": self.sharpness_max_purple,
        }

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine)
