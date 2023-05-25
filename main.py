from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"Hello": "Gracias Totales"}
