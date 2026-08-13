from domain.models import Country
from domain.ports import MarketDataGateway

# Contenedor para el resultado final
class ROIResult:
    def __init__(self, property_price, gross_annual_rent, estimated_expenses, net_annual_income, cap_rate, verdict):
        self.property_price = property_price
        self.gross_annual_rent = gross_annual_rent
        self.estimated_expenses = estimated_expenses
        self.net_annual_income = net_annual_income
        self.cap_rate = cap_rate
        self.verdict = verdict

class AnalyzeZipCodeCase:
    def __init__(self, data_gateway: MarketDataGateway):
        self.data_gateway = data_gateway

    def execute(self, zip_code: str, country: Country) -> ROIResult:
        # Aquí es donde le pedimos los datos al archivo de Zillow
        market_data = self.data_gateway.get_neighborhood_data(zip_code, country.value)
        
        annual_rent = market_data.average_rent * 12
        expenses = annual_rent * 0.35 # Asumimos 35% de gastos para USA
        net_income = annual_rent - expenses
        
        if market_data.average_price > 0:
            cap_rate = round((net_income / market_data.average_price) * 100, 2)
        else:
            cap_rate = 0.0

        if cap_rate >= 7.0:
            verdict = "Alta Rentabilidad (Cash Flow Ideal)."
        elif cap_rate >= 5.0:
            verdict = "Rentabilidad Moderada / Estable."
        else:
            verdict = "Mercado Sobrevalorado."

        return ROIResult(
            property_price=market_data.average_price,
            gross_annual_rent=annual_rent,
            estimated_expenses=expenses,
            net_annual_income=net_income,
            cap_rate=cap_rate,
            verdict=verdict
        )
