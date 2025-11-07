from fastapi.testclient import TestClient
from main import app, team, TEAMLIMIT

client = TestClient(app)

def setup_function():
    team.clear()

def test_health():
    """Verifica se a aplicação está saudavel."""
    setup_function()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_add_get_team():
    """Testa adicionar um Pokémon e depois listar o time."""
    setup_function()
    
    pokemon = {"nome": "Pikachu", "nivel": 25}
    responsePost = client.post("/team", json=pokemon)
    
    assert responsePost.status_code == 201
    data = responsePost.json()

    assert data["nome"] == "Pikachu"

    responseGet = client.get("/team")
    
    assert responseGet.status_code == 200
    data = responseGet.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Pikachu"

def test_team_limit():
    """Testa a lógica de negócio (limite de 6 Pokémon)."""
    setup_function()
    
    for i in range(TEAMLIMIT):
        client.post("/team", json={"nome": f"Pokemon-{i}", "nivel": 10})
    
    extraPokemonRequest = client.post("/team", json={"nome": "Extra", "nivel": 1})
    
    assert extraPokemonRequest.status_code == 400
    assert "O time está cheio" in extraPokemonRequest.json()["detail"]