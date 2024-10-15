from sqlalchemy.orm import Session
import models, schemas

def get_item(db: Session, item_id: str):
    return db.query(models.Item).filter(models.image_name == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_by_image_name(db: Session, image_name: str):
    return db.query(models.Item).filter(models.Item.image_name == image_name).first()

