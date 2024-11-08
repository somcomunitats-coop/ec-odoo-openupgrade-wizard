DELETE FROM ir_model_data where id in (SELECT
    ir_model_data.id
FROM
    ir_model_data
LEFT JOIN
    res_company
ON
    res_company.id = CAST(SPLIT_PART(ir_model_data.name, '_', 1) AS INTEGER)
WHERE
    ir_model_data.name ~ '^[0-9]+_' and res_company.id is null);


DELETE FROM account_payment_order WHERE id in (
    select account_payment_order.id 
    from account_payment_order 
    left join account_payment_line on account_payment_order.id = account_payment_line.order_id 
    where account_payment_line.order_id is null);