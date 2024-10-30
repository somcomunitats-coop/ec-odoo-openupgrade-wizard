import pathlib
import shutil

from odoo_openupgrade_wizard.tools.tools_postgres import ensure_database

from . import (
    assert_database,
    build_ctx_from_config_file,
    cli_runner_invoke,
    mock_odoo_rpc_url,
    move_to_test_folder,
)


def test_cli_dropdb(mocker):
    move_to_test_folder()
    mock_odoo_rpc_url(mocker)

    db_name = "database_test_cli___dropdb"
    ctx = build_ctx_from_config_file()

    # Ensure environment is clean
    ensure_database(ctx, db_name, state="absent")
    filestore_path = pathlib.Path(f"./filestore/filestore/{db_name}")
    shutil.rmtree(filestore_path, ignore_errors=True)

    # Initialize database
    cli_runner_invoke(["install-from-csv", f"--database={db_name}"])

    # Drop database
    cli_runner_invoke(["dropdb", f"--database={db_name}"])

    # Check database does not exists
    assert_database(ctx, db_name, "absent")

    # Check filestore does not exists
    assert not filestore_path.exists()
