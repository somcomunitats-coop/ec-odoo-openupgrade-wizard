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