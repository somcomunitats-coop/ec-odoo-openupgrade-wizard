import logging

_logger = logging.getLogger(__name__)
_logger.info("Executing post-migration.py script ...")

env = env  # noqa: F821

# Lista de módulos a desinstalar
modules_to_uninstall = ["base_rest_base_structure", "l10n_es_extra_data"]

# Actualizar lista de modulos
update_app_list = env["base.module.update"].create({})
update_app_list.update_module()

for module_name in modules_to_uninstall:
    try:
        # Desinstala el módulo
        module = env["ir.module.module"].search([("name", "=", module_name)], limit=1)
        if module and module.state == "installed":
            _logger.info(f"Uninstalling module: {module_name}")
            module.button_immediate_uninstall()
        else:
            _logger.warning(f"Module {module_name} not found or not installed.")
    except Exception as e:
        _logger.error(f"Error uninstalling module {module_name}: {e}")

# Confirma los cambios
env.cr.commit()
_logger.info("Module uninstallation completed.")

env.cr.commit()
