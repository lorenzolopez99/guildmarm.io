from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Armor(Base):
    __tablename__ = "armor"

    id = Column(Integer, primary_key=True,index=True)

    set_name = Column(String)
    slot = Column(String)

    skill1 = Column(String)
    skill1_count = Column(Integer)
    skill2 = Column(String)
    skill2_count = Column(Integer)

    gem_level_1 = Column(Integer)
    gem_level_2 = Column(Integer)
    gem_level_3 = Column(Integer)
    gem_level_4 = Column(Integer)
    #lowrank vs highrank vs masterrank?
    #Option to sort by in-game order?
    #materials?
    #group skill/ set skill?
    def to_dict(self):
        return {
            "id":self.id,
            "set_name":self.set_name,
            "slot": self.slot,
            "skill1": self.skill1,
            "skill1_count": self.skill1_count,
            "skill2": self.skill2,
            "skill2_count": self.skill2_count,
            "gem_level_1": self.gem_level_1,
            "gem_level_2": self.gem_level_2,
            "gem_level_3": self.gem_level_3,
            "gem_level_4": self.gem_level_4
        }

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine)
