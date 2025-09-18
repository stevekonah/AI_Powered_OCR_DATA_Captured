# Additional models for validated forms, audit trail

from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ValidatedForm(Base):
    __tablename__ = "validated_forms"
    id = Column(Integer, primary_key=True)
    scan_date = Column(DateTime, default=datetime.utcnow)
    form_type = Column(String)
    field_data = Column(JSON)
    approved_by = Column(String)
    approved_at = Column(DateTime)

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