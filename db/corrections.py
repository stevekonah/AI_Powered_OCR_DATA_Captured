from sqlalchemy import Column, Integer, String, JSON, DateTime
from .database import Base, Session
from datetime import datetime

class Correction(Base):
    __tablename__ = "corrections"
    id = Column(Integer, primary_key=True)
    form_type = Column(String)
    field_name = Column(String)
    image_path = Column(String)
    old_value = Column(String)
    corrected_value = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

def save_correction(form_type, field_name, image_path, old_value, corrected_value):
    session = Session()
    entry = Correction(
        form_type=form_type,
        field_name=field_name,
        image_path=image_path,
        old_value=old_value,
        corrected_value=corrected_value
    )
    session.add(entry)
    session.commit()
    session.close()