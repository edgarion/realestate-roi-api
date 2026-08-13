from fastapi.testclient import TestClient
from main import app

# Instanciamos el cliente de pruebas de FastAPI
client = TestClient(app)

# Datos de prueba genéricos
payload = {
    "country": "USA",
    "price": 500000,
    "monthly_rent": 3500
}

def test_roi_endpoint_rechaza_peticion_sin_api_key():
    # Act: Enviamos la petición sin cabeceras
    response = client.post("/v1/calculate-roi", json=payload)
    
    # Assert: Debe devolver Error 403 (Prohibido) o 401 (No autorizado)
    assert response.status_code in (401, 403)
    assert response.json()["detail"] == "Not authenticated"

def test_roi_endpoint_rechaza_peticion_con_api_key_invalida():
    # Act: Cabecera con una llave falsa
    headers = {"X-API-Key": "llave_falsa_hacker_123"}
    response = client.post("/v1/calculate-roi", json=payload, headers=headers)
    
    # Assert: Debe devolver Error 401
    assert response.status_code == 401
    assert response.json()["detail"] == "API Key inválida"

def test_roi_endpoint_acepta_peticion_con_api_key_valida():
    # Act: Cabecera con la llave correcta
    headers = {"X-API-Key": "sk_live_realestate_777"}
    response = client.post("/v1/calculate-roi", json=payload, headers=headers)
    
    # Assert: Debe procesar la petición y devolver 200 OK
    assert response.status_code == 200
    assert "ai_investment_verdict" in response.json()
