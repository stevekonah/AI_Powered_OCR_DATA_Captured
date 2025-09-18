from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///ocr_demo.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class AuditTrail(Base):
    __tablename__ = "audit_trail"
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer)
    table_name = Column(String)
    action = Column(String)
    changed_by = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    old_value = Column(JSON)
    new_value = Column(JSON)

def log_action(form_id, table_name, action, changed_by, old_value=None, new_value=None):
    session = Session()
    entry = AuditTrail(
        form_id=form_id, table_name=table_name, action=action,
        changed_by=changed_by, timestamp=datetime.utcnow(),
        old_value=old_value, new_value=new_value
    )
    session.add(entry)
    session.commit()
    session.close()