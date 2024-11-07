#!/bin/bash

# Verifica si se ha proporcionado el nombre de la base de datos como argumento
if [ -z "$1" ]; then
  echo "Uso: $0 <nombre_de_la_base_de_datos>"
  exit 1
fi

DATABASE=$1

# Desactiva ir_cron
odoo-openupgrade-wizard psql -d $DATABASE --command "update ir_cron set active = False;"

# Modifica smtp_host en ir_mail_server
odoo-openupgrade-wizard psql -d $DATABASE --command "update ir_mail_server set smtp_host = 'fake_' || smtp_host where 1=1;"

# Desactiva fetchmail_server
odoo-openupgrade-wizard psql -d $DATABASE --command "update fetchmail_server set active = False;"

# Modifica email en res_partner
odoo-openupgrade-wizard psql -d $DATABASE --command "update res_partner set email = 'fake_' || email where not email is null;"

# Modifica nombre y email en res_company
odoo-openupgrade-wizard psql -d $DATABASE --command "update res_company set name = '[PRE-PROD] ' || name, email = 'fake_' || email where 1=1;"

# Modifica nombre y apellidos en res_partner para socios de empresas
odoo-openupgrade-wizard psql -d $DATABASE --command "update res_partner set name = '[PRE-PROD] ' || name, lastname = '[PRE-PROD] ' || lastname, commercial_company_name = '[PRE-PROD] ' || commercial_company_name, display_name = '[PRE-PROD] ' || display_name where id in (select partner_id from res_company where 1=1);"