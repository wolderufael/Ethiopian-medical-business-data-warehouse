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
from typing import List, Optional,Dict

sys.path.append("app/")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create a folder for saving the detection results if it doesn't exist
os.makedirs("detected_images", exist_ok=True)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}

@app.get("/result/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# Image search and render endpoint
@app.get("/render/{image_name}",response_model=schemas.RenderResponse)
async def render_image(image_name: str, db: Session = Depends(get_db)):
    item = crud.get_item_by_image_name(db, image_name=image_name)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Split the coordinates and labels
    try:
        labels = item.labels.split(',')if item.labels else []
        confidences = list(map(float, item.confidences.split(','))) if item.confidences else []
        xmins = list(map(float, item.xmins.split(','))) if item.xmins else []
        ymins = list(map(float, item.ymins.split(','))) if item.ymins else []
        xmaxs = list(map(float, item.xmaxs.split(','))) if item.xmaxs else []
        ymaxs = list(map(float, item.ymaxs.split(','))) if item.ymaxs else []
        
        # Validate that all lists have the same length
        if not (len(labels) == len(confidences) == len(xmins) == len(ymins) == len(xmaxs) == len(ymaxs)):
            raise HTTPException(status_code=400, detail="Mismatch in number of labels and coordinates")

        # Load the image using OpenCV
        image_path = f"../data/Photo/{image_name}"  # Update with your image directory
        image = cv2.imread(image_path)

        # Draw bounding boxes and labels on the image
        for i in range(len(labels)):
            label = labels[i].strip()
            confidence = confidences[i] if confidences else 0
            xmin = int(xmins[i])
            ymin = int(ymins[i])
            xmax = int(xmaxs[i])
            ymax = int(ymaxs[i])

            # Draw the rectangle
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

            # Prepare the label text with confidence
            label_text = f"{label}: {confidence:.2f}"
            cv2.putText(image, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Convert image to byte array for return
        _, buffer = cv2.imencode('.jpg', image)
        img_byte_arr = io.BytesIO(buffer)

    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=400, detail=f"Error processing coordinates: {e}")

    # Return structured data and the image
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")
