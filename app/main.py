import sys
import os
import pickle
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, get_db
from fastapi.responses import FileResponse
import torch
import cv2
from PIL import Image
import numpy as np
import io

sys.path.append("app/")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Load the pre-trained YOLOv5 model
# Load the pre-trained logistic re model model using pickle
with open('../models/logistic_regression_model-09-10-2024-08-34-45-00.pkl', 'rb') as f:
    model = pickle.load(f)

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

# API route for object detection
@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    # Load the image file
    image_data = await file.read()

    # Convert the image file into an OpenCV image
    image = Image.open(io.BytesIO(image_data))
    image = np.array(image)

    # Perform object detection
    results = model(image)

    # Draw bounding boxes on the image using OpenCV
    results.render()  # This updates the image array with bounding boxes

    # Convert the updated image (with bounding boxes) to a format that can be returned
    output_image = Image.fromarray(image)
    output_path = f"detected_images/{file.filename}"

    # Save the output image to a file
    output_image.save(output_path)

    # Return the image with detections as a downloadable file
    return FileResponse(output_path, media_type="image/jpeg", filename=file.filename)