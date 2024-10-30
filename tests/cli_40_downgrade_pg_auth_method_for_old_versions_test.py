from . import cli_runner_invoke, move_to_test_folder


def test_cli_downgrade_pg_auth_method_for_old_versions():
    move_to_test_folder()

    cli_runner_invoke(
        [
            "init",
            "--project-name=test-cli-downgrade-auth-method",
            "--initial-version=12.0",
            "--final-version=13.0",
            "--postgresql-version=14",
        ],
    )

    move_to_test_folder()
    cli_runner_invoke(["get-code"])
    cli_runner_invoke(["docker-build", "--versions=12.0"])

    db_name = "database_test_cli-downgrade-auth-method__run"
    cli_runner_invoke(
        [
            "run",
            "--step=1",
            f"--database={db_name}",
            "--init-modules=base",
            "--stop-after-init",
        ],
    )
