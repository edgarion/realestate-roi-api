from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from domain.models import Country, Property
from domain.use_cases import CalculateROICase

router = APIRouter()

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

@router.post("/calculate-roi", response_model=ROIResponseDTO)
def calculate_roi_endpoint(data: PropertyDTO):
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
