from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.employee.repository.employee import EmployeeService
from app.employee.schema.employee import EmployeeResponse
from app.monitor.repository.monitor import MonitorService
from app.monitor.schema.monitor import LogCreate, LogsType
from db.database import get_db
from fastapi_pagination import Page, paginate, add_pagination

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
        monitor_service: MonitorService = Depends(get_monitor_service)
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
        key_employee, start_date, end_date)
    return paginate(results)
