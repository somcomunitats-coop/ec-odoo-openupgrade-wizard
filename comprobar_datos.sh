#!/bin/bash

# Verifica si se ha proporcionado el nombre de la base de datos como argumento
if [ -z "$1" ]; then
  echo "Uso: $0 <nombre_de_la_base_de_datos>"
  exit 1
fi

DATABASE=$1
OUTPUT_FILE="resultados.txt"

# Limpia el archivo de salida si ya existe
> "$OUTPUT_FILE"

# Ejecuta cada comando y redirige su salida al archivo de texto
{
  echo "Conteo de registros en ir_model:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM ir_model;"

  echo "Conteo de módulos instalados:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM ir_module_module WHERE state='installed';"

  echo "Conteo de compañías:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM res_company;"

  echo "Conteo de usuarios:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM res_users;"

  echo "Conteo de partners:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM res_partner;"

  echo "Conteo de impuestos:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM account_tax;"

  echo "Conteo de asientos contables:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM account_move;"

  echo "Conteo de órdenes de venta:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM sale_order;"

  echo "Resumen financiero por compañía:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "
  select count(distinct rc.id) as companies, count(am.id) as assentaments, 
  sum(aml.debit) as debit, sum(aml.credit) as credit, sum(aml.debit-aml.credit) as balance,
  sum(am.amount_total) total, sum(am.amount_untaxed) untaxed, sum(am.amount_tax) tax, sum(am.amount_residual) residual, 
  sum(am.amount_total_signed) total_signed, sum(am.amount_untaxed_signed) untaxed_signed, sum(am.amount_tax_signed) tax_signed, sum(am.amount_residual_signed) residual_signed
  from account_move as am 
  left join res_company as rc on rc.id = am.company_id 
  left join account_move_line aml on aml.move_id = am.id
  left join account_account aa on aa.id = aml.account_id 
  having  count(am.id) > 0;"

  echo "Resumen financiero por cuenta:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "
  select aa.code, aa.name, count(distinct rc.id) as companies, count(am.id) as assentaments, 
  sum(aml.debit) as debit, sum(aml.credit) as credit, sum(aml.debit-aml.credit) as balance,
  sum(am.amount_total) total, sum(am.amount_untaxed) untaxed, sum(am.amount_tax) tax, sum(am.amount_residual) residual, 
  sum(am.amount_total_signed) total_signed, sum(am.amount_untaxed_signed) untaxed_signed, sum(am.amount_tax_signed) tax_signed, sum(am.amount_residual_signed) residual_signed
  from account_move as am 
  left join res_company as rc on rc.id = am.company_id 
  left join account_move_line aml on aml.move_id = am.id
  left join account_account aa on aa.id = aml.account_id 
  group by aa.code, aa.name
  having  count(am.id) > 0;"

  echo "Resumen financiero detallado por compañía:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "
  select rc.id, rc.name, count(am.id) as assentaments, 
  sum(aml.debit) as debit, sum(aml.credit) as credit, sum(aml.debit-aml.credit) as balance,
  sum(am.amount_total) total, sum(am.amount_untaxed) untaxed, sum(am.amount_tax) tax, sum(am.amount_residual) residual, 
  sum(am.amount_total_signed) total_signed, sum(am.amount_untaxed_signed) untaxed_signed, sum(am.amount_tax_signed) tax_signed, sum(am.amount_residual_signed) residual_signed
  from account_move as am 
  left join res_company as rc on rc.id = am.company_id 
  left join account_move_line aml on aml.move_id = am.id
  left join account_account aa on aa.id = aml.account_id 
  group by rc.id
  having  count(am.id) > 0
  order by rc.\"name\" asc;"

  echo "Resumen financiero detallado por compañía y cuenta:"
  odoo-openupgrade-wizard psql -d $DATABASE --command "
  select rc.id as rc_id, rc.name, aa.id as aa_id, aa.code, aa.name, count(am.id) as assentaments, 
  sum(aml.debit) as debit, sum(aml.credit) as credit, sum(aml.debit-aml.credit) as balance,
  sum(am.amount_total) total, sum(am.amount_untaxed) untaxed, sum(am.amount_tax) tax, sum(am.amount_residual) residual, 
  sum(am.amount_total_signed) total_signed, sum(am.amount_untaxed_signed) untaxed_signed, sum(am.amount_tax_signed) tax_signed, sum(am.amount_residual_signed) residual_signed
  from account_move as am 
  left join res_company as rc on rc.id = am.company_id 
  left join account_move_line aml on aml.move_id = am.id
  left join account_account aa on aa.id = aml.account_id 
  group by rc.id, aa_id, aa.code, aa.name
  having  count(am.id) > 0
  order by rc.\"name\" asc, aa.code;"
} >> "$OUTPUT_FILE"
