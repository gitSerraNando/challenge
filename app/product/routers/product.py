from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.monitor.repository.monitor import MonitorService
from app.product.repository.product import ProductService
from app.product.schema.product import ProductResponse, SalesSummary
from app.user.models import User
from app.utils.oauth import get_current_user
from db.database import get_db

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)


def get_monitor_service(db: Session = Depends(get_db)) -> MonitorService:
    return MonitorService(db)


@router.get("/sales_per_product/", response_model=Page[ProductResponse])
async def sales_per_product(
        key_product: str = Query(..., example="40702"),
        start_date: date = Query(..., example="2023-11-29"),
        end_date: date = Query(..., example="2023-11-30"),
        db: Session = Depends(get_db),
        monitor_service: MonitorService = Depends(get_monitor_service),
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve the sales per product within a specified date range.

    Args:
    - key_product (str): The key of the product.
    - start_date (date): The start date of the date range.
    - end_date (date): The end date of the date range.
    - db (Session): The database session.
    - monitor_service (MonitorService): The monitor service.

    Returns:
    - Page[ProductResponse]: The paginated sales per product results.
    """
    product_service = ProductService(db, monitor_service)
    results = product_service.sales_per_product(
        key_product, start_date, end_date, current_user)
    return paginate(results)


@router.get("/sales_summary/", response_model=SalesSummary)
def read_sales_summary(key_product: str = Query(..., example="40702"), db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user),
                       monitor_service: MonitorService = Depends(get_monitor_service), ):
    """
    Retrieve the sales summary for the current user.

    Parameters:
    - db (Session): The database session.
    - current_user (User): The current user.
    - monitor_service (MonitorService): The monitor service.

    Returns:
    - SalesSummary: The sales summary for the current user.
    """
    product_service = ProductService(db, monitor_service)
    return product_service.get_sales_summary(current_user, key_product)
