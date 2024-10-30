from pathlib import Path
from shutil import copy

from odoo_openupgrade_wizard.tools.tools_postgres import (
    ensure_database,
    execute_sql_request,
)

from . import (
    build_ctx_from_config_file,
    cli_runner_invoke,
    move_to_test_folder,
)


def test_cli_upgrade():
    move_to_test_folder()
    ctx = build_ctx_from_config_file()

    for n in ["01", "02"]:
        copy(
            Path(
                f"../extra_script/{n}-post-migration-custom_test.py"
            ).absolute(),
            Path(
                "scripts/step_01__regular__14.0/"
                f"{n}-post-migration-custom_test.py"
            ),
        )

    # Initialize database
    db_name = "database_test_cli___upgrade"
    ensure_database(ctx, db_name, state="absent")

    cli_runner_invoke(
        [
            "run",
            "--step=1",
            f"--database={db_name}",
            "--init-modules=base",
            "--stop-after-init",
        ],
    )

    # Ensure that 'base' module is installed at 14.0
    request = (
        "SELECT latest_version"
        " FROM ir_module_module"
        " WHERE state ='installed'"
        " AND name='base';"
    )
    latest_version = execute_sql_request(ctx, request, database=db_name)

    assert latest_version[0][0].startswith("14.")

    cli_runner_invoke(
        [
            "upgrade",
            f"--database={db_name}",
            "--first-step=1",
            "--last-step=3",
        ],
    )

    # Ensure that 'base' module is installed at 15.0
    request = (
        "SELECT latest_version"
        " FROM ir_module_module"
        " WHERE state ='installed'"
        " AND name='base';"
    )
    latest_version = execute_sql_request(ctx, request, database=db_name)

    assert latest_version[0][0].startswith("15.")

    # ensure the first post-migration-custom scripts have been executed
    request = (
        "SELECT name"
        " FROM res_partner"
        " WHERE name like 'Post Script 1 - Partner #%';"
    )

    result = execute_sql_request(ctx, request, database=db_name)
    assert len(result) == 10

    # ensure the second post-migration-custom scripts have been executed
    request = (
        "SELECT name"
        " FROM res_partner"
        " WHERE name = 'Post Script 2 - Partner #1';"
    )

    result = execute_sql_request(ctx, request, database=db_name)
    assert len(result) == 1
