from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///ocr_demo.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Example placeholder model; add your other models here as needed
class ValidatedForm(Base):
    __tablename__ = "validated_forms"
    id = Column(Integer, primary_key=True)
    form_type = Column(String)
    field_data = Column(JSON)

def init_db():
    Base.metadata.create_all(engine)

import random

def get_random_validated(sample_size=5):
    session = Session()
    all_validated = session.query(ValidatedForm).all()
    samples = random.sample(all_validated, min(sample_size, len(all_validated)))
    session.close()
    return samples
