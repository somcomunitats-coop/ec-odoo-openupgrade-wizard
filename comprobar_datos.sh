#!/bin/bash

# Verifica si se ha proporcionado el nombre de la base de datos como argumento
if [ -z "$1" ]; then
  echo "Uso: $0 <nombre_de_la_base_de_datos>"
  exit 1
fi

DATABASE=$1


odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM ir_model;"

odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM ir_module_module WHERE state='installed';"

odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM res_company;"

odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM res_users;"

odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM res_partner;"

odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM account_tax;"

odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM account_move;"

odoo-openupgrade-wizard psql -d $DATABASE --command "SELECT count(*) FROM sale_order;"

odoo-openupgrade-wizard psql -d $DATABASE --command "select count(distinct rc.id) as companies, count(am.id) as assentaments, 
sum(aml.debit) as debit, sum(aml.credit) as credit, sum(aml.debit-aml.credit) as balance,
sum(am.amount_total) total, sum(am.amount_untaxed) untaxed, sum(am.amount_tax) tax, sum(am.amount_residual) residual, 
sum(am.amount_total_signed) total_signed, sum(am.amount_untaxed_signed) untaxed_signed, sum(am.amount_tax_signed) tax_signed, sum(am.amount_residual_signed) residual_signed
from account_move as am 
left join res_company as rc on rc.id = am.company_id 
left join account_move_line aml on aml.move_id = am.id
left join account_account aa on aa.id = aml.account_id 
having  count(am.id) > 0;"

odoo-openupgrade-wizard psql -d $DATABASE --command "select aa.code, aa.name, count(distinct rc.id) as companies, count(am.id) as assentaments, 
sum(aml.debit) as debit, sum(aml.credit) as credit, sum(aml.debit-aml.credit) as balance,
sum(am.amount_total) total, sum(am.amount_untaxed) untaxed, sum(am.amount_tax) tax, sum(am.amount_residual) residual, 
sum(am.amount_total_signed) total_signed, sum(am.amount_untaxed_signed) untaxed_signed, sum(am.amount_tax_signed) tax_signed, sum(am.amount_residual_signed) residual_signed
from account_move as am 
left join res_company as rc on rc.id = am.company_id 
left join account_move_line aml on aml.move_id = am.id
left join account_account aa on aa.id = aml.account_id 
group by aa.code, aa.name
having  count(am.id) > 0;"


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
order by rc."name" asc;"

odoo-openupgrade-wizard psql -d $DATABASE --command "
select rc.id as rc_id, rc.name, aa.id as aa_id, aa.code, aa.name, count(am.id) as assentaments, 
sum(aml.debit) as debit, sum(aml.credit) as credit, sum(aml.debit-aml.credit) as balance,
sum(am.amount_total) total, sum(am.amount_untaxed) untaxed, sum(am.amount_tax) tax, sum(am.amount_residual) residual, 
sum(am.amount_total_signed) total_signed, sum(am.amount_untaxed_signed) untaxed_signed, sum(am.amount_tax_signed) tax_signed, sum(am.amount_residual_signed) residual_signed
from account_move as am 
left join res_company as rc on rc.id = am.company_id 
left join account_move_line aml on aml.move_id = am.id
left join account_account aa on aa.id = aml.account_id 
--where rc.id = 127 and (aa.code ilike '62900%' or aa.id = 72863 )
group by rc.id, aa_id, aa.code, aa.name
having  count(am.id) > 0
order by rc."name" asc, aa.code;"