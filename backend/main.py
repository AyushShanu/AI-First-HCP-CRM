from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import traceback

from database import engine, get_db, Base
import models, schemas
import agent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First HCP CRM")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/hcps")
def list_hcps(db: Session = Depends(get_db)):
    return db.query(models.HCP).all()

@app.get("/interactions")
def list_interactions(db: Session = Depends(get_db)):
    return db.query(models.Interaction).order_by(models.Interaction.created_at.desc()).all()

@app.post("/interactions", response_model=schemas.InteractionOut)
def create_interaction(payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    rec = models.Interaction(**payload.model_dump())
    db.add(rec); db.commit(); db.refresh(rec)
    return rec

@app.put("/interactions/{iid}", response_model=schemas.InteractionOut)
def update_interaction(iid: int, payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    rec = db.query(models.Interaction).get(iid)
    if not rec:
        raise HTTPException(404, "Not found")
    for k, v in payload.model_dump().items():
        setattr(rec, k, v)
    db.commit(); db.refresh(rec)
    return rec

@app.post("/chat")
def chat(req: schemas.ChatRequest):
    try:
        reply = agent.run_agent(req.message, req.session_id)

        print("MAIN:", agent.LAST_EXTRACTED)

        return {
            "reply": reply,
            "form": agent.LAST_EXTRACTED.get("form"),
            "interaction_id": agent.LAST_EXTRACTED.get("interaction_id"),
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))