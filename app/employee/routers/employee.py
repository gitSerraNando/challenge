from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.employee.repository.employee import EmployeeService
from app.monitor.repository.monitor import MonitorService
from app.monitor.schema.monitor import LogCreate, LogsType
from db.database import get_db

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


def get_monitor_service(db: Session = Depends(get_db)) -> MonitorService:
    return MonitorService(db)


@router.get("/sales_per_employee/")
async def sales_per_employee(
        key_employee: str,
        start_date: date = Query(...),
        end_date: date = Query(...),
        db: Session = Depends(get_db),
        monitor_service: MonitorService = Depends(get_monitor_service)
):
    employee_service = EmployeeService(db, monitor_service)
    try:
        return employee_service.sales_per_employee(key_employee, start_date, end_date)
    except Exception as e:
        log_data = LogCreate(level=LogsType.ERROR, message=str(e))
        monitor_service.create_log(log_data)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
