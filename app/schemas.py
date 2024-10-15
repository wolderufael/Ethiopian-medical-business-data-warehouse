# from pydantic import BaseModel

# class ItemCreate(BaseModel):
#     title: str
#     description: str


# class Item(BaseModel):
#     id: int
#     title: str
#     description: str


#     class Config:
#         from_attributes = True

from pydantic import BaseModel
from typing import List, Optional

class ItemCreate(BaseModel):
    image_name: str
    labels: Optional[str]  # Comma-separated names of detected objects
    confidences: Optional[str]  # Comma-separated confidence scores
    xmins: Optional[str]  # Comma-separated xmin coordinates
    ymins: Optional[str]  # Comma-separated ymin coordinates
    xmaxs: Optional[str]  # Comma-separated xmax coordinates
    ymaxs: Optional[str]  # Comma-separated ymax coordinates

# Define the schema for reading an item (with id)
class Item(BaseModel):
    image_name: str  # Primary key field
    labels: Optional[str] # Detected object labels
    confidences: Optional[str]  # Confidence scores
    xmins: Optional[str]  # X minimum coordinates
    ymins: Optional[str]  # Y minimum coordinates
    xmaxs: Optional[str]  # X maximum coordinates
    ymaxs: Optional[str]  # Y maximum coordinates


    class Config:
        orm_mode = True  # Allows Pydantic to work with ORM models
