from sqlalchemy import Column, Integer, String,ARRAY,Float,MetaData,Table
from database import Base,engine

#  Define metadata
metadata = MetaData()

# Reflect the existing table using the engine
object_detection_table = Table('object_detection', metadata, autoload_with=engine)



class Item(Base):
    __tablename__ = "object_detection"
    # __table_args__ = {'autoload': True}
        

    image_name = Column(String, primary_key=True, index=True)
    labels=Column(String, index=True) # comma separated name of detected objects	
    confidences=Column(String, index=True)	# comma separated confidence score of each detected object in the image
    xmins=Column(String, index=True)
    ymins=Column(String, index=True)
    xmaxs=Column(String, index=True)	
    ymaxs=Column(String, index=True)
  
