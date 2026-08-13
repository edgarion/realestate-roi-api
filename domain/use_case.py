from domain.models import Country, Property, ROIResult

class CalculateROICase:
    EXPENSE_RATES = {
        Country.USA: 0.35,
        Country.AUSTRALIA: 0.25,
        Country.UK: 0.20
    }

    def execute(self, prop: Property) -> ROIResult:
        annual_rent = prop.monthly_rent * 12

        if prop.annual_expenses and prop.annual_expenses > 0:
            expenses = prop.annual_expenses
        else:
            rate = self.EXPENSE_RATES.get(prop.country, 0.25)
            expenses = annual_rent * rate

        net_income = annual_rent - expenses
        cap_rate = round((net_income / prop.price) * 100, 2)

        if cap_rate >= 7.0:
            verdict = "High Yield Investment Opportunity"
        elif cap_rate >= 5.0:
            verdict = "Moderate Investment / Stable Cash Flow"
        else:
            verdict = "Low Yield / Appreciation Focused"

        return ROIResult(
            country=prop.country,
            property_price=prop.price,
            gross_annual_rent=annual_rent,
            estimated_expenses=expenses,
            net_annual_income=net_income,
            cap_rate=cap_rate,
            verdict=verdict
        )
