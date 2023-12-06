BEGIN
    EXECUTE IMMEDIATE CONCAT(
        'CREATE OR REPLACE VIEW `mide-lo-que-importa-279017.celes.total_and_average_sales_per_employee` AS ',
        'SELECT REPLACE(KeyEmployee, "1|", "") AS KeyEmployee, ',
        'ROUND(SUM(Amount), 2) AS TotalSales, ',
        'ROUND(AVG(Amount), 2) AS AverageSales ',
        'FROM `mide-lo-que-importa-279017.celes.callegen` ',
        'WHERE Qty >= 0 AND Amount >= 0 AND CostAmount >= 0 AND DiscAmount >= 0 AND ',
        'NOT (KeyEmployee IS NULL OR KeyDate IS NULL OR KeySale IS NULL OR KeyCurrency IS NULL) ',
        'GROUP BY KeyEmployee'
    );
END