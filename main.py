from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import spotipy

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

app = FastAPI(
    title="Utpl Interoperabilidad APP",
    description= description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Cristian Bravo",
        "url": "http://x-force.example.com/contact/",
        "email": "cpbravo3@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

class Jugar(BaseModel):
    id: int
    nombre: str
    edad: int
    equipo: Optional[str] = None
    minutos_jugados: str

jugarList = []

@app.post("/jugar", response_model=Jugar)
def crear_jugar(jugador: Jugar):
    jugarList.append(jugador)
    return jugador

@app.get("/jugadores", response_model=List[Jugar])
def get_jugadores():
    return jugarList

@app.get("/jugadores/{jugador_id}", response_model=Jugar)
def obtener_jugador(jugador_id: int):
    for jugador in jugarList:
        if jugador.id == jugador_id:
            return jugador
    raise HTTPException(status_code=404, detail="Jugador no encontrado")

@app.delete("/jugadores/{jugador_id}")
def eliminar_jugador(jugador_id: int):
    for index, jugador in enumerate(jugarList):
        if jugador.id == jugador_id:
            jugarList.pop(index)
            return {"message": "Jugador eliminado"}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")

@app.get("/pista/{pista_id}")
async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track

@app.get("/artistas/{artista_id}")
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista


@app.get("/")
def read_root():
    return {"Hello": "Gracias Totales"}
