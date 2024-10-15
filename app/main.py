import sys
import os
import pickle
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, get_db
from fastapi.responses import FileResponse,StreamingResponse
import torch
import cv2
from PIL import Image, ImageDraw
import numpy as np
import io

sys.path.append("app/")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create a folder for saving the detection results if it doesn't exist
os.makedirs("detected_images", exist_ok=True)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}

# @app.post("/items/", response_model=schemas.Item)
# def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return crud.create_item(db=db, item=item)

@app.get("/result/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# @app.get("/items/{item_id}", response_model=schemas.Item)
# def read_item(item_id: int, db: Session = Depends(get_db)):
#     db_item = crud.get_item(db, item_id=item_id)
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item

# Image search and render endpoint
@app.get("/render/{image_name}",response_model=schemas.Item)
def render_image(image_name: str, db: Session = Depends(get_db)):
    # Fetch the record from the database
    item = crud.get_item_by_image_name(db, image_name=image_name)
    if item is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Load the image from the local folder
    image_path = f"../data/Photo/{image_name}"  # Ensure the image exists in this folder
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image file not found")

    # Get bounding box coordinates from the database
    xmins = list(map(int, item.xmins.split(',')))
    ymins = list(map(int, item.ymins.split(',')))
    xmaxs = list(map(int, item.xmaxs.split(',')))
    ymaxs = list(map(int, item.ymaxs.split(',')))
    labels = item.labels.split(',')

    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    for xmin, ymin, xmax, ymax, label in zip(xmins, ymins, xmaxs, ymaxs, labels):
        draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=3)
        draw.text((xmin, ymin), label, fill="red")

    # Save the modified image to memory
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # Return the image as a streaming response
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")


async def render_image(image_name: str, db: Session = Depends(get_db)):
    item = crud.get_item_by_image_name(db, image_name=image_name)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Split the coordinates and labels
    try:
        labels = item.labels.split(',')
        xmins = list(map(float, item.xmins.split(',')))
        ymins = list(map(float, item.ymins.split(',')))
        xmaxs = list(map(float, item.xmaxs.split(',')))
        ymaxs = list(map(float, item.ymaxs.split(',')))
        
        # Construct a list of dictionaries to pair labels with their coordinates
        detections: List[Dict[str, float]] = []
        for i in range(len(labels)):
            detection = {
                "label": labels[i].strip(),
                "xmin": xmins[i],
                "ymin": ymins[i],
                "xmax": xmaxs[i],
                "ymax": ymaxs[i],
            }
            detections.append(detection)
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=400, detail=f"Error processing coordinates: {e}")

    # Return structured data
    return {
        "image_name": item.image_name,
        "detections": detections
    }