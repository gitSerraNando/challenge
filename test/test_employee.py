import pytest
from unittest.mock import Mock, patch
from datetime import date
from app.employee.repository.employee import EmployeeService
from app.monitor.repository.monitor import MonitorService
from app.user.models import User
from fastapi import HTTPException, status
from app.employee.schema.employee import EmployeeResponse, SalesSummary
from datetime import datetime



fake_key_employee = '123'
fake_start_date = date(2021, 1, 1)
fake_end_date = date(2021, 1, 31)
fake_current_user = User(user_type='Admin')
fake_total_sales = 100.0
fake_average_sales = 100.0
fake_response_data = [{
    "KeyEmployee": fake_key_employee,
    "KeyDate": fake_start_date.strftime('%Y-%m-%d'),
    "KeySale": "some_key_sale",
    "KeyCurrency": "1|COP",
    "Qty": 10,
    "Amount": 100.0,
    "CostAmount": 50.0,
    "DiscAmount": 0.0
}]
fake_response_data_sales_summary = {
    "KeyEmployee": fake_key_employee,
    "TotalSales": 100.0,
    "AverageSales": 100.0
}


@pytest.fixture
def mock_monitor_service():
    return Mock(spec=MonitorService)

@pytest.fixture
def mock_db_session():
    return Mock()

@pytest.fixture
def mock_bigquery_client():
    mock_client = Mock()
    patcher = patch('app.employee.repository.employee.client', mock_client)
    patcher.start()
    yield mock_client
    patcher.stop()


class MockBigQueryRow:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'KeyDate' and isinstance(value, str):
                self.__dict__[key] = datetime.strptime(value, '%Y-%m-%d').date()
            else:
                self.__dict__[key] = value

    def get(self, key, default=None):
        return getattr(self, key, default)



class TestEmployeeService:

    def test_sales_per_employee_success(self, mock_db_session, mock_monitor_service, mock_bigquery_client):
        mock_results = [MockBigQueryRow(**row) for row in fake_response_data]

        mock_query_job = mock_bigquery_client.query.return_value
        mock_query_job.result.return_value = iter(mock_results)

        employee_service = EmployeeService(mock_db_session, mock_monitor_service)

        result = employee_service.sales_per_employee(fake_key_employee, fake_start_date, fake_end_date, fake_current_user)

        assert result == fake_response_data
        mock_bigquery_client.query.assert_called_once()

    def test_sales_per_employee_unauthorized(self,mock_db_session, mock_monitor_service, mock_bigquery_client):
        fake_current_user = User(user_type='User')

        employee_service = EmployeeService(mock_db_session, mock_monitor_service)

        with pytest.raises(HTTPException) as exc_info:
            employee_service.sales_per_employee(fake_key_employee, fake_start_date, fake_end_date, fake_current_user)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    def test_get_sales_summary_success(self, mock_db_session, mock_monitor_service, mock_bigquery_client):
        mock_query_job = mock_bigquery_client.query.return_value
        mock_query_job.result.return_value = iter([MockBigQueryRow(**fake_response_data_sales_summary)])

        employee_service = EmployeeService(mock_db_session, mock_monitor_service)

        result = employee_service.get_sales_summary(fake_current_user, fake_key_employee)

        assert result == SalesSummary(
            KeyEmployee=fake_response_data_sales_summary["KeyEmployee"],
            TotalSales=fake_response_data_sales_summary["TotalSales"],
            AverageSales=fake_response_data_sales_summary["AverageSales"]
        )
        mock_bigquery_client.query.assert_called_once()

    def test_get_sales_summary_unauthorized(self,mock_db_session, mock_monitor_service, mock_bigquery_client):
        fake_current_user = User(user_type='User')

        employee_service = EmployeeService(mock_db_session, mock_monitor_service)

        with pytest.raises(HTTPException) as exc_info:
            employee_service.get_sales_summary(fake_current_user, fake_key_employee)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    def test_get_sales_summary_error(self,mock_db_session, mock_monitor_service, mock_bigquery_client):
        mock_query_job = mock_bigquery_client.query.return_value
        mock_query_job.result.return_value = []

        employee_service = EmployeeService(mock_db_session, mock_monitor_service)

        with pytest.raises(HTTPException) as exc_info:
            employee_service.get_sales_summary(fake_current_user, fake_key_employee)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR