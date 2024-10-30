import pathlib
import shutil

from odoo_openupgrade_wizard.tools.tools_postgres import ensure_database

from . import (
    build_ctx_from_config_file,
    cli_runner_invoke,
    mock_odoo_rpc_url,
    move_to_test_folder,
)


def test_cli_dumpdb(mocker):
    move_to_test_folder()
    mock_odoo_rpc_url(mocker)

    # Initialize database
    db_name = "database_test_cli___dumpdb"
    ctx = build_ctx_from_config_file()
    ensure_database(ctx, db_name, state="absent")

    cli_runner_invoke(["install-from-csv", f"--database={db_name}"])

    # Dump database and filestore
    formatlist = [("p", "d"), ("c", "tgz"), ("t", "t"), ("d", "d")]
    for formats in formatlist:
        database_path = pathlib.Path("database_test_cli___dumpdb")
        filestore_path = pathlib.Path("database_test_clie___dumpdb.filestore")

        assert not database_path.exists()
        assert not filestore_path.exists()

        cli_runner_invoke(
            [
                "--log-level=DEBUG",
                "dumpdb",
                f"--database={db_name}",
                f"--database-path={database_path}",
                f"--database-format={formats[0]}",
                f"--filestore-path={filestore_path}",
                f"--filestore-format={formats[1]}",
            ],
        )

        assert database_path.exists()
        assert filestore_path.exists()

        # Cleanup files
        if database_path.is_dir():
            shutil.rmtree(database_path)
        else:
            database_path.unlink()

        if filestore_path.is_dir():
            shutil.rmtree(filestore_path)
        else:
            filestore_path.unlink()


def test_cli_dumpdb_failure(mocker):
    move_to_test_folder()
    mock_odoo_rpc_url(mocker)

    # Initialize database
    db_name = "database_test_cli___dumpdb"
    ctx = build_ctx_from_config_file()
    ensure_database(ctx, db_name, state="absent")

    cli_runner_invoke(
        [
            "--log-level=DEBUG",
            "install-from-csv",
            f"--database={db_name}",
        ],
    )

    # First dump
    formats = ("d", "d")
    database_path = pathlib.Path("database_test_cli___dumpdb")
    filestore_path = pathlib.Path("database_test_clie___dumpdb.filestore")

    assert not database_path.exists()
    assert not filestore_path.exists()

    cli_runner_invoke(
        [
            "--log-level=DEBUG",
            "dumpdb",
            f"--database={db_name}",
            f"--database-path={database_path}",
            f"--database-format={formats[0]}",
            f"--filestore-path={filestore_path}",
            f"--filestore-format={formats[1]}",
        ],
    )

    assert database_path.exists()
    assert filestore_path.exists()

    # With same name
    cli_runner_invoke(
        [
            "--log-level=DEBUG",
            "dumpdb",
            f"--database={db_name}",
            f"--database-path={database_path}",
            f"--database-format={formats[0]}",
            f"--filestore-path={filestore_path}",
            f"--filestore-format={formats[1]}",
        ],
        expect_success=False,
    )

    # With --force
    cli_runner_invoke(
        [
            "--log-level=DEBUG",
            "dumpdb",
            f"--database={db_name}",
            f"--database-path={database_path}",
            f"--database-format={formats[0]}",
            f"--filestore-path={filestore_path}",
            f"--filestore-format={formats[1]}",
            "--force",
        ],
    )

    # With name outside of project path
    cli_runner_invoke(
        [
            "--log-level=DEBUG",
            "dumpdb",
            f"--database={db_name}",
            f"--database-path=/{database_path}",
            f"--database-format={formats[0]}",
            f"--filestore-path=/{filestore_path}",
            f"--filestore-format={formats[1]}",
        ],
        expect_success=False,
    )

    # With a non-existing database
    cli_runner_invoke(
        [
            "--log-level=DEBUG",
            "dumpdb",
            "--database=database_test_cli___dumpdb_non_existing",
            f"--database-path={database_path}",
            f"--database-format={formats[0]}",
            f"--filestore-path={filestore_path}",
            f"--filestore-format={formats[1]}",
        ],
        expect_success=False,
    )

    # Cleanup files
    if database_path.is_dir():
        shutil.rmtree(database_path)
    else:
        database_path.unlink()

    if filestore_path.is_dir():
        shutil.rmtree(filestore_path)
    else:
        filestore_path.unlink()
