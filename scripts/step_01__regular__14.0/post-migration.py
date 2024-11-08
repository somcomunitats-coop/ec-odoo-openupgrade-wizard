import logging

_logger = logging.getLogger(__name__)
_logger.info("Executing post-migration.py script ...")

env = env  # noqa: F821

# Lista de módulos a desinstalar
modules_to_uninstall = [
    "account_menu",
    "account_statement_import_txt_xlsx",
    "base_rest_auth_jwt",
    "mass_editing",
    "web_access_rule_buttons",
    "account_reconciliation_widget",
    "web_decimal_numpad_dot",
    "base_future_response",
    "cooperator_website",
    "contract_queue_job",
    "contract_mandate",
]

for module_name in modules_to_uninstall:
    try:
        # Desinstala el módulo
        module = env['ir.module.module'].search([('name', '=', module_name)], limit=1)
        if module and module.state == 'installed':
            _logger.info(f"Uninstalling module: {module_name}")
            module.button_immediate_uninstall()
        else:
            _logger.warning(f"Module {module_name} not found or not installed.")
    except Exception as e:
        _logger.error(f"Error uninstalling module {module_name}: {e}")

# Confirma los cambios
env.cr.commit()
_logger.info("Module uninstallation completed.")

payments = env['account.payment'].search([('payment_line_ids', '=', False),('payment_order_id', '!=', False)])
_logger.info(f"Check payments : {len(payments)}")
for payment in payments:
    try:
        if len(payment.payment_line_ids) == 0:
            _logger.info(f"Delete payment : {payment.id}")
            payment.unlink()
    except Exception as e:
        _logger.error(f"Error delete payment {payment.id}: {e}")

# Confirma los cambios
env.cr.commit()
_logger.info("Payments without payment lines deleted.")

companies = env['res.company'].search([])
_logger.info(f"Check companies : {len(companies)}")
for company in companies:
    try:
        wizard = env['wizard.update.charts.accounts'].with_context(default_company_id=company.id).create()
        wizard.action_find_records()
        wizard.action_update_records()
        _logger.info(f"Update chart templates for companie : {company.id} - {company.name}")
    except Exception as e:
        _logger.error(f"Error update chart templates {company.id} - {company.name}: {e}")

# Confirma los cambios
env.cr.commit()
_logger.info("Update chart templates of all companies")