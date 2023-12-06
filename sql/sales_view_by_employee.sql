BEGIN
       EXECUTE IMMEDIATE CONCAT(
        'CREATE OR REPLACE VIEW `mide-lo-que-importa-279017.celes.sales_view_by_employee` AS ',
        'SELECT REPLACE(KeyEmployee, "1|", "") AS KeyEmployee, KeyDate, KeySale, KeyCurrency, Qty, Amount, CostAmount, DiscAmount ',
        'FROM `mide-lo-que-importa-279017.celes.callegen` ',
        'WHERE Qty >= 0 AND Amount >= 0 AND CostAmount >= 0 AND DiscAmount >= 0 AND ',
        'NOT (KeyEmployee IS NULL OR KeyDate IS NULL OR KeySale IS NULL OR KeyCurrency IS NULL)'
    );
END