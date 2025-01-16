# app/api/group.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.group import Group
from ..schemas import GroupCreate, Group
from ..database import engine, Base

router = APIRouter()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/{group_id}", response_model=Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(group)
    db.commit()
    return {"detail": "Group deleted"}

@router.get("/", response_model=List[Group])
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()
