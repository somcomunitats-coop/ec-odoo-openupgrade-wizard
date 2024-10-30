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


def test_cli_restoredb(mocker):
    move_to_test_folder()
    mock_odoo_rpc_url(mocker)

    db_name = "database_test_cli___restoredb"
    ctx = build_ctx_from_config_file()

    # Ensure environment is clean
    ensure_database(ctx, db_name, state="absent")
    dest_filestore_path = pathlib.Path(f"./filestore/filestore/{db_name}")
    shutil.rmtree(dest_filestore_path, ignore_errors=True)

    # Copy database and filestore data in a accessible folder
    database_path = pathlib.Path("./restoredb.dump")
    filestore_path = pathlib.Path("./restoredb.tar.gz")

    shutil.copyfile(pathlib.Path("../restoredb/test.dump"), database_path)
    shutil.copyfile(pathlib.Path("../restoredb/test.tar.gz"), filestore_path)

    cli_runner_invoke(
        [
            "restoredb",
            f"--database={db_name}",
            f"--database-path={database_path}",
            "--database-format=c",
            f"--filestore-path={filestore_path}",
            "--filestore-format=tgz",
        ],
    )

    # check filestore exists
    assert dest_filestore_path.exists()

    # Check database exists
    assert_database(ctx, db_name, "present")

    # Delete filestore and database
    shutil.rmtree(dest_filestore_path)
    ensure_database(ctx, db_name, state="absent")
