from datetime import date

from fastapi import HTTPException, status
from google.api_core.exceptions import GoogleAPIError
from google.cloud import bigquery
from sqlalchemy.orm import Session

from app.monitor.repository.monitor import MonitorService
from app.monitor.schema.monitor import LogCreate, LogsType
from db.database import client


class EmployeeService:
    def __init__(self, db: Session, monitor_service: MonitorService):
        self.db = db
        self.monitor_service = monitor_service

    def sales_per_employee(self, key_employee: str, start_date: date, end_date: date):
        if start_date > end_date:
            log_data = LogCreate(
                level=LogsType.WARNING,
                message=f"Detail: sales_per_employee :The start date must be before the end date - Response: {status.HTTP_400_BAD_REQUEST}")
            self.monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The start date must be before the end date"
            )

        query = """
            SELECT KeyEmployee, KeyDate, KeySale, Qty, Amount, CostAmount, DiscAmount
            FROM `mide-lo-que-importa-279017.celes.sales_view_by_employee`
            WHERE KeyEmployee = @key_employee AND 
                KeyDate BETWEEN @start_date AND @end_date
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "key_employee", "STRING", key_employee),
                bigquery.ScalarQueryParameter(
                    "start_date", "DATE", start_date),
                bigquery.ScalarQueryParameter("end_date", "DATE", end_date)
            ]
        )

        try:
            query_job = client.query(query, job_config=job_config)
            results = query_job.result()
            return [dict(row) for row in results]
        except GoogleAPIError as e:
            log_data = LogCreate(level=LogsType.ERROR,
                                 message=f"Error en BigQuery: {e.message}")
            self.monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al ejecutar la consulta en BigQuery."
            )
        except Exception as e:
            log_data = LogCreate(level=LogsType.ERROR,
                                 message=f"Error inesperado: {e}")
            self.monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Un error inesperado ocurrió."
            )
