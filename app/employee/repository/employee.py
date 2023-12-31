from datetime import date
from typing import List

from fastapi import HTTPException, status
from google.api_core.exceptions import GoogleAPIError
from google.cloud import bigquery
from sqlalchemy.orm import Session

from app.employee.schema.employee import EmployeeResponse, SalesSummary
from app.monitor.repository.monitor import MonitorService
from app.monitor.schema.monitor import LogCreate, LogsType
from app.user.models import User
from db.database import client


class EmployeeService:
    def __init__(self, db: Session, monitor_service: MonitorService):
        self.db = db
        self.monitor_service = monitor_service

    def sales_per_employee(self, key_employee: str, start_date: date, end_date: date, current_user: User) -> List[
        EmployeeResponse]:
        if 'Admin' in current_user.user_type:
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
                response_data = []
                for row in results:
                    row_data = {
                        "KeyEmployee": row.KeyEmployee,
                        "KeyDate": row.KeyDate.strftime('%Y-%m-%d') if row.KeyDate else None,
                        "KeySale": row.KeySale,
                        "KeyCurrency": row.get('KeyCurrency', '1|COP'),
                        "Qty": row.Qty,
                        "Amount": row.Amount,
                        "CostAmount": row.CostAmount,
                        "DiscAmount": row.DiscAmount
                    }
                    response_data.append(row_data)

                return response_data
            except GoogleAPIError as e:
                log_data = LogCreate(level=LogsType.ERROR,
                                     message=f"Error en BigQuery: {e.message}")
                self.monitor_service.create_log(log_data)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error executing query in BigQuery."
                )
            except Exception as e:
                log_data = LogCreate(level=LogsType.ERROR,
                                     message=f"Unexpected error: {e}")
                self.monitor_service.create_log(log_data)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred."
                )

        else:
            log_data = LogCreate(
                level=LogsType.WARNING,
                message=f"Detail: You do not have permission to view this information! - Response: {status.HTTP_403_FORBIDDEN}")
            self.monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this information!")

    def get_sales_summary(self, current_user: User, key_employee: str) -> List[SalesSummary]:
        if 'Admin' in current_user.user_type:
            query = """
                    SELECT * FROM `mide-lo-que-importa-279017.celes.total_and_average_sales_per_employee`
                    WHERE KeyEmployee = @key_employee
                """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "key_employee", "STRING", key_employee)], )
            query_job = client.query(query, job_config=job_config)
            try:
                result = next(query_job.result(), None)
                if result:
                    return SalesSummary(
                        KeyEmployee=result.KeyEmployee,
                        TotalSales=result.TotalSales,
                        AverageSales=result.AverageSales,

                    )
                else:
                    log_data = LogCreate(
                        level=LogsType.WARNING,
                        message=f"Detail: No sales summary found for the specified employee - Response: {status.HTTP_404_NOT_FOUND}")
                    self.monitor_service.create_log(log_data)
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No sales summary found for the specified employee."
                    )
            except GoogleAPIError as e:
                log_data = LogCreate(level=LogsType.ERROR,
                                     message=f"Error en BigQuery: {e.message}")
                self.monitor_service.create_log(log_data)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error executing query in BigQuery."
                )
            except Exception as e:
                log_data = LogCreate(level=LogsType.ERROR,
                                     message=f"Unexpected error: {e}")
                self.monitor_service.create_log(log_data)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred."
                )
        else:
            log_data = LogCreate(
                level=LogsType.WARNING,
                message=f"Detail: You do not have permission to view this information! - Response: {status.HTTP_403_FORBIDDEN}")
            self.monitor_service.create_log(log_data)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this information!")
