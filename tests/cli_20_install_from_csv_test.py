from odoo_openupgrade_wizard.tools.tools_postgres import (
    ensure_database,
    execute_sql_request,
)

from . import (
    build_ctx_from_config_file,
    cli_runner_invoke,
    mock_odoo_rpc_url,
    move_to_test_folder,
)


def test_cli_install_from_csv(mocker):
    move_to_test_folder()
    mock_odoo_rpc_url(mocker)

    # Initialize database
    db_name = "database_test_cli___install_from_csv"
    ctx = build_ctx_from_config_file()

    ensure_database(ctx, db_name, state="absent")

    cli_runner_invoke(["install-from-csv", f"--database={db_name}"])

    # Ensure that 'base' is installed
    request = (
        "SELECT count(*)"
        " FROM ir_module_module"
        " WHERE state ='installed'"
        " AND name in ('base');"
    )
    module_qty = int(execute_sql_request(ctx, request, database=db_name)[0][0])

    assert module_qty == 1

    # Ensure that 'account' is not installed
    request = (
        "SELECT count(*)"
        " FROM ir_module_module"
        " WHERE state ='installed'"
        " AND name in ('account');"
    )
    module_qty = int(execute_sql_request(ctx, request, database=db_name)[0][0])

    assert module_qty == 0
