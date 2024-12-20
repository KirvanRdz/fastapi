from fastapi import Path, Query, Request,HTTPException,Depends, APIRouter
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from user_jwt import  validate_token
from database.database import session
from models.movies import MovieModel

routerMovie= APIRouter()

class BearerJwt(HTTPBearer):
    async def  __call__(self, request:Request):
        auth= await super().__call__(request)
        data= validate_token(auth.credentials)
        if data["email"] != "user@example.com":
            raise HTTPException(status_code=403, detail="No esta autorizado")
        
class Movie(BaseModel):
    title:str = Field(default='Titulo de la pelicula', max_length=25,min_length=5)
    overview: str = Field(default='Descripación de la pelicula', max_length=50,min_length=5)
    year: int = Field(default=2024)
    rating: float

@routerMovie.get('/movie/{id}', status_code=200, dependencies=[Depends(BearerJwt())], tags=['Movie'])
def get_movie(id: int = Path(ge=1, le=5)):
    db = session()
    data=db.query(MovieModel).filter(MovieModel.id==id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pelicula no encotrada")
    return {'data': jsonable_encoder(data)}

@routerMovie.get('/movies', status_code=200, dependencies=[Depends(BearerJwt())], tags=['Movie'])
def get_movie():
    db = session()
    data=db.query(MovieModel).all()
    
    return {'data': jsonable_encoder(data)}

@routerMovie.post('/movie', status_code=201, tags=['Movie'])
def create_movie(movie:Movie):
    db = session()
    newMovie= MovieModel(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    return {'movie':movie}

@routerMovie.put('/movie/{id}', status_code=200, tags=['Movie'])
def update_movie(movie: Movie, id: int):
    db = session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Pelicula no encotrada")
    
    # Actualizar los campos
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating

    # Confirmar los cambios
    db.commit()
    db.refresh(data)  # Refrescar para obtener el estado actualizado del objeto

    # Convertir a un formato serializable
    return {'data': jsonable_encoder(data)}

@routerMovie.delete('/movie/{id}', status_code=200, tags=['Movie'])
def delete_movie(id:int):
    db = session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Pelicula no encotrada")
    
    db.delete(data)

    # Confirmar los cambios
    db.commit()

    return {'message': 'Movie eliminada'}
    
    