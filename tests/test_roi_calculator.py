from domain.models import Country, Property
from domain.use_cases import CalculateROICase

def test_calculate_roi_usa_default_expenses():
    # Preparar datos (Propiedad en USA sin gastos definidos)
    property_data = Property(
        country=Country.USA,
        price=500000.0,
        monthly_rent=3500.0
    )
    use_case = CalculateROICase()

    # Ejecutar
    result = use_case.execute(property_data)

    # Verificar
    assert result.cap_rate == 5.46
    assert result.verdict == "Moderate Investment / Stable Cash Flow"

def test_calculate_roi_uk_custom_expenses():
    # Preparar datos (Propiedad en UK con gastos explícitos)
    property_data = Property(
        country=Country.UK,
        price=250000.0,
        monthly_rent=2000.0,
        annual_expenses=3000.0
    )
    use_case = CalculateROICase()

    # Ejecutar
    result = use_case.execute(property_data)

    # Verificar (24000 de renta - 3000 gastos = 21000 neto. 21000/250000 = 8.4%)
    assert result.cap_rate == 8.4
    assert result.verdict == "High Yield Investment Opportunity"
