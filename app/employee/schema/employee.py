from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class EmployeeResponse(BaseModel):
    KeyEmployee: str
    KeyDate: str
    KeySale: str
    KeyCurrency: Optional[str]
    Qty: float
    Amount: float
    CostAmount: float
    DiscAmount: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "KeyEmployee": "17585",
                "KeyDate": "2023-11-29",
                "KeySale": "E8DD6EA2-C48E-EE11-BD48-78E3B5B056E8|A47D1BFE-C48E-EE11-BD48-78E3B5B056E8",
                "KeyCurrency": "1|COP",
                "Qty": 2.0,
                "Amount": 5800.0,
                "CostAmount": 2717.16,
                "DiscAmount": 0.0,


            }
        }


class SalesSummary(BaseModel):
    KeyEmployee: str
    TotalSales: float
    AverageSales: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "KeyEmployee": "17585",
                "TotalSales": 5800,
                "AverageSales": 5800.0,


            }
        }
