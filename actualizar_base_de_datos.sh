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
odoo-openupgrade-wizard psql -d $DATABASE --command "update ir_mail_server set active = False;"

# Desactiva fetchmail_server
odoo-openupgrade-wizard psql -d $DATABASE --command "update fetchmail_server set active = False;"
