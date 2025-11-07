from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API de Time Pokemon (Demo CI/CD)",
    description="Um projeto para demonstrar um pipeline completo de GitOps."
)

class PokemonCreate(BaseModel):
    """Modelo de dados para criar um novo Pokémon."""
    nome: str
    nivel: int

class Pokemon(BaseModel):
    """Modelo de dados para retornar um Pokémon (com ID)."""
    id: int
    nome: str
    nivel: int

# Variveis globais, guardam os valores em memória
team: Dict[int, Pokemon] = {}
lastId = 0
TEAMLIMIT = 6

@app.get("/")
async def root():
    """Rota principal com uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo à API de Time Pokémon! Acesse /docs para ver a documentação."}

@app.get("/health")
async def health():
    """Rota de saúde."""
    return {"status": "OK", "version": "1.1"}

@app.get("/team", response_model=List[Pokemon])
async def getTeam():
    """Retorna todos os Pokémon no time."""
    return list(team.values())

@app.post("/team", response_model=Pokemon, status_code=201)
async def addTeam(newPokemon: PokemonCreate):
    """Adiciona um novo Pokémon ao time."""
    global team
    global lastId

    if len(team) >= TEAMLIMIT:
        raise HTTPException(status_code=400, detail="O time está cheio! (Máximo 6 pokemon).")
    
    createdPokemon = Pokemon(id=lastId, **newPokemon.model_dump())
    team[lastId] = createdPokemon
    lastId += 1

    return createdPokemon