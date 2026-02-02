from db.database import engine, SessionLocal
from db.models import Resource
from api.data import RESOURCES
from datetime import datetime

def parse_dt(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def seed():
    session = SessionLocal()

    for r in RESOURCES:
        r = {k: parse_dt(v) if k in ["extracted_at", "transformed_at", "enriched_at"] else v for k, v in r.items()}
        session.merge(Resource(**r))

    session.commit()
    session.close()
    print("✅ Database seeded")

if __name__ == "__main__":
    from db.database import Base
    Base.metadata.create_all(bind=engine)
    seed()
