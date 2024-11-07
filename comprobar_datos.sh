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