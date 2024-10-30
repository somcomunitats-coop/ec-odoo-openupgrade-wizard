import logging
import os
from pathlib import Path

import yaml
from click.testing import CliRunner
from plumbum.cmd import mkdir

from odoo_openupgrade_wizard.cli.cli import main
from odoo_openupgrade_wizard.tools.tools_postgres import execute_sql_request

_logger = logging.getLogger()


def assert_result_cli_invoke(result):
    pass


def move_to_test_folder():
    """function to call at the beginning at the tests
    to change the current working directory.
    Note : this function is idempotens, to avoid to generate errors
    if many tests scripts are executed.
    """
    if os.getcwd().endswith("tests/data/output"):
        return
    test_folder_path = Path("tests/data/output")
    mkdir([test_folder_path, "--parents"])
    os.chdir(test_folder_path)


def cli_runner_invoke(cmd, expect_success=True):
    if not cmd:
        cmd = []
    cmd = ["--log-level=DEBUG"] + cmd
    try:
        result = CliRunner().invoke(
            main,
            args=cmd,
            catch_exceptions=False,
        )
        if expect_success:
            if not result.exit_code == 0:
                _logger.error("exit_code: %s" % result.exit_code)
                _logger.error("output: %s" % result.output)
            assert result.exit_code == 0
        else:
            assert result.exit_code != 0
    except Exception as exception:
        if Path("log").exists():
            log_files = [
                Path("log") / Path(f)
                for f in os.listdir(Path("log"))
                if f[-4:] == ".log"
            ]
            for log_file in log_files:
                print("============================")
                print(log_file)
                print("============================")
                _f = open(log_file)
                print(_f.read())
                _f.close()
                print("============================")
            raise exception


def build_ctx_from_config_file() -> dict:
    env_folder_path = Path(".")

    class context:
        pass

    ctx = context()
    setattr(ctx, "obj", {})
    config_file_path = env_folder_path / "config.yml"
    if not config_file_path.exists():
        raise Exception(
            "Configuration file not found %s" % config_file_path.absolute()
        )
    with open(config_file_path) as file:
        config = yaml.safe_load(file)
        ctx.obj["config"] = config
        file.close()

    ctx.obj["env_folder_path"] = env_folder_path
    ctx.obj["src_folder_path"] = env_folder_path / Path("src")
    return ctx


def mock_odoo_rpc_url(mocker):
    """Mock the _ODOO_RPC_URL for testing purpose"""
    odoo_rpc_url = os.environ.get("ODOO_RPC_URL")
    if odoo_rpc_url:
        mocker.patch(
            "odoo_openupgrade_wizard.tools.tools_odoo_instance._ODOO_RPC_URL",
            odoo_rpc_url,
        )


def assert_database(ctx, db_name, state):
    request = "select datname FROM pg_database WHERE datistemplate = false;"
    results = execute_sql_request(ctx, request)
    if state == "present":
        assert [db_name] in results
    else:
        assert [db_name] not in results
