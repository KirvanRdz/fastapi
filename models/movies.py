from database.database import Base
from sqlalchemy import Float, String, Integer , Column

class MovieModel(Base):
    __tablename__='movies'
    id= Column(Integer, primary_key=True)
    title= Column(String)
    overview= Column(String)
    year= Column(Integer)
    rating= Column(Float)
