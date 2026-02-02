# db/models.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from db.database import Base

class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(String, primary_key=True, index=True)
    resource_name = Column(String, nullable=False)
    source_url = Column(String, nullable=False)

    domain = Column(String, index=True)
    category = Column(String)
    category_slug = Column(String, index=True)

    resource_type = Column(String, index=True)
    skill_cluster = Column(String, index=True)

    domain_weight = Column(Integer, default=0)
    is_github = Column(Boolean, default=False)

    extracted_at = Column(DateTime)
    transformed_at = Column(DateTime)
    enriched_at = Column(DateTime)   # ✅ REQUIRED
