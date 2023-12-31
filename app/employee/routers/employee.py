from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.employee.repository.employee import EmployeeService
from app.employee.schema.employee import EmployeeResponse, SalesSummary
from app.monitor.repository.monitor import MonitorService
from app.user.models import User
from app.utils.oauth import get_current_user
from db.database import get_db

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


def get_monitor_service(db: Session = Depends(get_db)) -> MonitorService:
    return MonitorService(db)


@router.get("/sales_per_employee/", response_model=Page[EmployeeResponse])
async def sales_per_employee(
        key_employee: str = Query(..., example="17585"),
        start_date: date = Query(..., example="2023-11-29"),
        end_date: date = Query(..., example="2023-11-30"),
        db: Session = Depends(get_db),
        monitor_service: MonitorService = Depends(get_monitor_service),
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve the sales per employee within a specified date range.

    Args:
    - key_employee (str): The key of the employee.
    - start_date (date): The start date of the date range.
    - end_date (date): The end date of the date range.
    - db (Session): The database session.
    - monitor_service (MonitorService): The monitor service.

    Returns:
    - Page[EmployeeResponse]: The paginated sales per employee results.
    """
    employee_service = EmployeeService(db, monitor_service)
    results = employee_service.sales_per_employee(
        key_employee, start_date, end_date, current_user)
    return paginate(results)


@router.get("/sales_summary/", response_model=SalesSummary)
def read_sales_summary(key_employee: str = Query(..., example="17585"), db: Session = Depends(get_db),
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
    employee_service = EmployeeService(db, monitor_service)
    return employee_service.get_sales_summary(current_user, key_employee)
