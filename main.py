from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from fastapi_versioning import VersionedFastAPI, version

import spotipy
import uuid
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth import authenticate

#importar libreria mongoDb
import pymongo

client = pymongo.MongoClient("mongodb+srv://userCB123:Cpbomax1989@cluster0.kddef5q.mongodb.net/?retryWrites=true&w=majority")
database = client["ejemploDB"]
coleccion = database["jugadores"]

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='030dfbeeb23345d084575346f635465b',
    client_secret='4ca662fd4d5e4430bc75a3d36692afcc'
))

description = """
Utpl tnteroperabilidad API ayuda a describir las capacidades de un directorio. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Crear info artista** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name":"jugadores",
        "description": "Permite realizar un crud completo de jugadores (listar)"
    }
]

app = FastAPI(
    title="Utpl Interoperabilidad APP",
    description= description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Cristian Bravo",
        "url": "https://github.com/crash8992",
        "email": "cpbravo3@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata
)

#para agregar seguridad a nuestro api
security = HTTPBasic()

class JugadorRepos (BaseModel):
    id: str
    nombre: str
    edad: int
    equipo: Optional[str] = None
    min_jugados: int

class JugadorIngreso (BaseModel):
    nombre: str
    edad: int
    equipo: Optional[str] = None
    min_jugados: int

class JugadorEntradaV2 (BaseModel):
    nombre: str
    edad: int
    equipo: str
    min_jugados: int
    

jugadorList = []

@app.post("/jugadores", response_model=JugadorRepos, tags = ["jugadores"])
@version(1, 0)
async def crear_jugador(player: JugadorIngreso):
    itemJugador = JugadorRepos(id=str(uuid.uuid4()), nombre= player.nombre, edad = player.edad, equipo = player.equipo, min_jugados = player.min_jugados)
    result = coleccion.insert_one(itemJugador.dict())
    return itemJugador

@app.post("/jugadores", response_model=JugadorEntradaV2, tags = ["jugadores"])
@version(2, 0)
async def crear_jugadorv2(playerE: JugadorEntradaV2):
    itemJugador = JugadorRepos (id= str(uuid.uuid4()), nombre= playerE.nombre, edad = playerE.edad, equipo = playerE.equipo, min_jugados = playerE.min_jugados)
    resultadoDB =  coleccion.insert_one(itemJugador.dict())
    return itemJugador

@app.get("/jugadores", response_model=List[JugadorRepos], tags=["jugadores"])
@version(1, 0)
def get_jugadores():
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/jugadores/{jugador_id}", response_model=JugadorRepos , tags=["jugadores"])
@version(1, 0)
def obtener_jugador (jugador_id: str):
    item = coleccion.find_one({"id": jugador_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    

@app.delete("/jugador/{jugador_id}", tags=["jugadores"])
@version(1, 0)
def eliminar_jugador (jugador_id: str):    
    result = coleccion.delete_one({"id": jugador_id})
    if result.deleted_count == 1:
        return {"mensaje": "Jugador eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Jugador NO encontrada")

@app.get("/pista/{pista_id}")
@version(1, 0)
async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track

@app.get("/artistas/{artista_id}")
@version(1, 0)
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista


@app.get("/")
def read_root():
    return {"Hello": "Gracias Totales"}

app = VersionedFastAPI(app)
