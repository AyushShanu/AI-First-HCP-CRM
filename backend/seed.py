from database import SessionLocal, engine, Base
from models import HCP

Base.metadata.create_all(bind=engine)
db = SessionLocal()
if not db.query(HCP).count():
    db.add_all([
        HCP(name="Dr. Anjali Sharma", specialty="Oncology", hospital="Apollo Hospital"),
        HCP(name="Dr. John Smith", specialty="Cardiology", hospital="City Care"),
        HCP(name="Dr. Meera Patel", specialty="Neurology", hospital="Fortis"),
    ])
    db.commit()
    print("Seeded HCPs ✅")
db.close()
