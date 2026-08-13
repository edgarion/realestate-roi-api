from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class MarketData:
    average_price: float
    average_rent: float

class MarketDataGateway(ABC):
    @abstractmethod
    def get_neighborhood_data(self, zip_code: str, country: str) -> MarketData:
        pass
