from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import sqlite3

app = FastAPI()

conn = sqlite3.connect('databaseCB.db')
cursor = conn.cursor()

class Jugador(BaseModel):
    id: int
    nombre: str
    edad: int
    equipo: Optional[str] = None
    minutos_jugados: Optional[float] = None

create_table_query = '''
    CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        edad INTEGER,
        equipo TEXT,
        minutos_jugados REAL
    )
'''
cursor.execute(create_table_query)
conn.commit()

@app.post("/jugadores", response_model=Jugador)
def crear_jugador(jugador: Jugador):
    insert_query = '''
        INSERT INTO jugadores (id, nombre, edad, equipo, minutos_jugados)
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (jugador.id, jugador.nombre, jugador.edad, jugador.equipo, jugador.minutos_jugados))
    conn.commit()
    return jugador

@app.get("/jugadores", response_model=List[Jugador])
def get_jugadores():
    select_query = '''
        SELECT id, nombre, edad, equipo, minutos_jugados
        FROM jugadores
    '''
    cursor.execute(select_query)
    jugadores = []
    for row in cursor.fetchall():
        id, nombre, edad, equipo, minutos_jugados = row
        jugadores.append(Jugador(id=id, nombre=nombre, edad=edad, equipo=equipo, minutos_jugados=minutos_jugados))
    return jugadores

@app.get("/jugadores/{jugador_id}", response_model=Jugador)
def obtener_jugador(jugador_id: int):
    select_query = '''
        SELECT id, nombre, edad, equipo, minutos_jugados
        FROM jugadores
        WHERE id = ?
    '''
    cursor.execute(select_query, (jugador_id,))
    jugador = cursor.fetchone()
    if jugador:
        id, nombre, edad, equipo, minutos_jugados = jugador
        return Jugador(id=id, nombre=nombre, edad=edad, equipo=equipo, minutos_jugados=minutos_jugados)
    raise HTTPException(status_code=404, detail="Jugador no encontrado")

@app.on_event("shutdown")
def shutdown_event():
    conn.close()
