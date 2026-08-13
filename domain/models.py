from enum import Enum
from typing import Optional
from dataclasses import dataclass

class Country(str, Enum):
    USA = "USA"
    UK = "UK"
    AUSTRALIA = "AU"

@dataclass
class Property:
    country: Country
    price: float
    monthly_rent: float
    annual_expenses: Optional[float] = None

@dataclass
class ROIResult:
    country: Country
    property_price: float
    gross_annual_rent: float
    estimated_expenses: float
    net_annual_income: float
    cap_rate: float
    verdict: str
