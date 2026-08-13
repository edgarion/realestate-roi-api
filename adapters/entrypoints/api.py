import os
from fastapi import APIRouter, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from domain.models import Country
from domain.use_cases import AnalyzeZipCodeCase
from adapters.outbound.market_data import ZillowDataGateway

router = APIRouter()

api_key_header = APIKeyHeader(name="X-RapidAPI-Proxy-Secret", auto_error=True)

# 2. El portero compara la contraseña con la que guardaste en Render
async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("PROXY_SECRET"):
        raise HTTPException(status_code=401, detail="API Key inválida")
    return api_key
    
# ¡MIRA AQUÍ! Ahora FastAPI sabe que debe esperar un zip_code
class ZipCodeRequestDTO(BaseModel):
    country: Country
    zip_code: str = Field(..., description="Ejemplo: 33139")

class ROIResponseDTO(BaseModel):
    zip_code_analyzed: str
    average_property_price: float
    average_monthly_rent: float
    cap_rate_percentage: float
    market_intelligence_verdict: str

@router.post("/analyze-market", response_model=ROIResponseDTO)
def analyze_market_endpoint(data: ZipCodeRequestDTO, api_key: str = Security(verify_api_key)):
    try:
        # Conectamos Zillow con nuestro cerebro
        zillow_gateway = ZillowDataGateway()
        use_case = AnalyzeZipCodeCase(data_gateway=zillow_gateway)
        
        result = use_case.execute(zip_code=data.zip_code, country=data.country)

        return ROIResponseDTO(
            zip_code_analyzed=data.zip_code,
            average_property_price=result.property_price,
            average_monthly_rent=result.gross_annual_rent / 12,
            cap_rate_percentage=result.cap_rate,
            market_intelligence_verdict=result.verdict
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
