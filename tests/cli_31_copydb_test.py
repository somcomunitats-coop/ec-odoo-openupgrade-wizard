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


def test_cli_copydb(mocker):
    move_to_test_folder()
    mock_odoo_rpc_url(mocker)

    db_name = "database_test_cli___copydb"
    db_dest_name = "database_test_cli___copydb__copy"
    ctx = build_ctx_from_config_file()

    # Ensure environment is clean
    ensure_database(ctx, db_name, state="absent")
    dest_filestore_path = pathlib.Path(f"./filestore/filestore/{db_dest_name}")
    shutil.rmtree(dest_filestore_path, ignore_errors=True)

    # Initialize database
    cli_runner_invoke(["install-from-csv", f"--database={db_name}"])

    # Copy database
    cli_runner_invoke(
        [
            "copydb",
            f"--source={db_name}",
            f"--dest={db_dest_name}",
        ],
    )

    # check filestore exists
    assert dest_filestore_path.exists()

    # Check database exists
    assert_database(ctx, db_dest_name, "present")

    # Delete filestore and database
    shutil.rmtree(dest_filestore_path)
    ensure_database(ctx, db_dest_name, state="absent")
