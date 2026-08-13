from domain.ports import MarketDataGateway, MarketData
import httpx

class ZillowDataGateway(MarketDataGateway):
    def get_neighborhood_data(self, zip_code: str, country: str) -> MarketData:
        print(f"Buscando precios reales en Zillow para el ZIP {zip_code}...")

        # 1. La URL base limpia (sin los filtros del final)
        url = "https://zillow-com-live-data-scraper-api.p.rapidapi.com/bylocation" 
        
        # 2. Aquí le inyectamos automáticamente el código postal que nos pida la IA
        querystring = {
            "location": zip_code, 
            "listType": "for-sale"
        }

        # 3. Tus credenciales exactas (actualizadas con el nuevo host)
        headers = {
            "X-RapidAPI-Key": "fb3b4ac7e4msh0fbf162ecd0c9bfp17a2b4jsn91ccb01a4dd0",
            "X-RapidAPI-Host": "zillow-com-live-data-scraper-api.p.rapidapi.com"
        }

        try:
            response = httpx.get(url, headers=headers, params=querystring, timeout=15.0)
            data = response.json()
            
            # Buscamos la lista de propiedades en la respuesta
            casas = data.get("props", data.get("results", data.get("data", [])))
            
            if not casas:
                print("No se encontraron casas, usando datos por defecto.")
                return MarketData(average_price=400000.0, average_rent=2500.0)

            total_price = sum(casa.get("price", 0) for casa in casas if casa.get("price", 0) > 0)
            count = sum(1 for casa in casas if casa.get("price", 0) > 0)

            if count == 0:
                return MarketData(average_price=400000.0, average_rent=2500.0)

            precio_medio = total_price / count
            alquiler_estimado = precio_medio * 0.006 

            print(f"Éxito: Precio medio calculado para {zip_code}: ${precio_medio}")
            return MarketData(average_price=precio_medio, average_rent=alquiler_estimado)

        except Exception as e:
            print(f"Error de conexión con Zillow RapidAPI: {e}")
            return MarketData(average_price=400000.0, average_rent=2500.0)
