from fastapi import APIRouter, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from typing import Optional
from domain.models import Country, Property
from domain.use_cases import CalculateROICase

router = APIRouter()

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY_NAME = "X-API-Key"
# auto_error=True hará que FastAPI lance un 403 automático si la cabecera no existe
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Base de datos simulada de claves válidas
VALID_API_KEYS = {"sk_live_realestate_777", "sk_test_123"}

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida"
        )
    return api_key

# --- ESQUEMAS DTO ---
class PropertyDTO(BaseModel):
    country: Country
    price: float = Field(..., gt=0)
    monthly_rent: float = Field(..., gt=0)
    annual_expenses: Optional[float] = Field(None, ge=0)

class ROIResponseDTO(BaseModel):
    country: str
    property_price: float
    gross_annual_rent: float
    estimated_expenses: float
    net_annual_income: float
    cap_rate_percentage: float
    ai_investment_verdict: str

# --- ENDPOINT PROTEGIDO ---
# Añadimos la dependencia de seguridad inyectando api_key
@router.post("/calculate-roi", response_model=ROIResponseDTO)
def calculate_roi_endpoint(
    data: PropertyDTO, 
    api_key: str = Security(verify_api_key) # <-- BARRERA DE SEGURIDAD
):
    try:
        domain_property = Property(
            country=data.country,
            price=data.price,
            monthly_rent=data.monthly_rent,
            annual_expenses=data.annual_expenses
        )
        use_case = CalculateROICase()
        result = use_case.execute(domain_property)

        return ROIResponseDTO(
            country=result.country.value,
            property_price=result.property_price,
            gross_annual_rent=result.gross_annual_rent,
            estimated_expenses=result.estimated_expenses,
            net_annual_income=result.net_annual_income,
            cap_rate_percentage=result.cap_rate,
            ai_investment_verdict=result.verdict
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
