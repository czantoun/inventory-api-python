from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from typing import List
import jwt

# Database setup
DATABASE_URL = "postgresql://postgres:admin@localhost/inventory_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Inventory model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    quantity = Column(Integer)
    
# Pydantic model for serialization
class ItemOut(BaseModel):
    id: int
    name: str
    description: str
    quantity: int

    class Config:
        orm_mode = True  # Enables SQLAlchemy model compatibility

Base.metadata.create_all(bind=engine)

# Pydantic schemas
class ItemCreate(BaseModel):
    name: str
    description: str
    quantity: int

class ItemUpdate(BaseModel):
    name: str = None
    description: str = None
    quantity: int = None

# FastAPI setup
app = FastAPI()

# Authentication setup
SECRET_KEY = "your_secret_key"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory API!"}

@app.post("/items/", response_model=dict)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"id": db_item.id, "message": "Item created successfully"}

@app.get("/items/", response_model=List[ItemOut])
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()  # Fetch all items from the database
    return items  # FastAPI will serialize the list of items to JSON

@app.get("/items/{item_id}", response_model=dict)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "description": item.description, "quantity": item.quantity}

@app.put("/items/{item_id}", response_model=dict)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item updated successfully"}

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}
