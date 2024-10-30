import datetime
import logging
import sys
from pathlib import Path

import click
import yaml
from click_loglevel import LogLevel
from loguru import logger

import odoo_openupgrade_wizard
from odoo_openupgrade_wizard.cli.cli_copydb import copydb
from odoo_openupgrade_wizard.cli.cli_docker_build import docker_build
from odoo_openupgrade_wizard.cli.cli_dropdb import dropdb
from odoo_openupgrade_wizard.cli.cli_dumpdb import dumpdb
from odoo_openupgrade_wizard.cli.cli_estimate_workload import estimate_workload
from odoo_openupgrade_wizard.cli.cli_execute_script_python import (
    execute_script_python,
)
from odoo_openupgrade_wizard.cli.cli_execute_script_sql import (
    execute_script_sql,
)
from odoo_openupgrade_wizard.cli.cli_generate_module_analysis import (
    generate_module_analysis,
)
from odoo_openupgrade_wizard.cli.cli_get_code import get_code
from odoo_openupgrade_wizard.cli.cli_init import init
from odoo_openupgrade_wizard.cli.cli_install_from_csv import install_from_csv
from odoo_openupgrade_wizard.cli.cli_psql import psql
from odoo_openupgrade_wizard.cli.cli_pull_submodule import pull_submodule
from odoo_openupgrade_wizard.cli.cli_restoredb import restoredb
from odoo_openupgrade_wizard.cli.cli_run import run
from odoo_openupgrade_wizard.cli.cli_upgrade import upgrade
from odoo_openupgrade_wizard.tools.tools_system import ensure_folder_exists

DEFAULT_CONFIG_FILE = "config.yml"
DEFAULT_MODULES_FILE = "modules.csv"


@click.group()
@click.version_option(version=odoo_openupgrade_wizard.__version__)
@click.option(
    "--env-folder",
    default="./",
    type=click.Path(
        exists=True,
        file_okay=False,
        writable=True,
        resolve_path=True,
    ),
    help="Folder that will contains all the configuration of the wizard"
    " and all the Odoo code required to make the migrations. Let empty to"
    " use current folder (./).",
)
@click.option(
    "-c",
    "--config-file",
    type=click.Path(
        exists=True,
        file_okay=True,
    ),
    help=(
        f"Configuration file to use. By default, a file named "
        f'"{DEFAULT_CONFIG_FILE}" in the environment folder will be used.'
    ),
)
@click.option(
    "--modules-file",
    type=click.Path(
        exists=True,
        file_okay=True,
    ),
    help=(
        f"Modules file to use. By default, a file named "
        f'"{DEFAULT_MODULES_FILE}" in the environment folder will be used.'
    ),
)
@click.option(
    "--filestore-folder",
    type=click.Path(
        exists=True, file_okay=False, writable=True, resolve_path=True
    ),
    help="Folder that contains the Odoo filestore of the database(s)"
    " to migrate. Let empty to use the subfolder 'filestore' of the"
    " environment folder.",
)
@click.option("-l", "--log-level", type=LogLevel(), default=logging.INFO)
@click.pass_context
def main(
    ctx, env_folder, config_file, modules_file, filestore_folder, log_level
):
    """
    Provides a command set to perform odoo Community Edition migrations.
    """
    date_begin = datetime.datetime.now()
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logger.debug(f"Beginning script '{ctx.invoked_subcommand}' ...")
    if not isinstance(ctx.obj, dict):
        ctx.obj = {}

    # Define all the folder required by the tools
    env_folder_path = Path(env_folder)
    src_folder_path = env_folder_path / Path("./src/")
    if filestore_folder:
        filestore_folder_path = filestore_folder
    else:
        filestore_folder_path = env_folder_path / "filestore"

    script_folder_path = env_folder_path / Path("./scripts/")
    log_folder_path = env_folder_path / Path("./log/")

    # ensure log folder exists
    ensure_folder_exists(log_folder_path, git_ignore_content=True)

    # Create log file
    log_prefix = "{}__{}".format(
        date_begin.strftime("%Y_%m_%d__%H_%M_%S"), ctx.invoked_subcommand
    )
    log_file_path = log_folder_path / Path(log_prefix + ".log")
    logger.add(log_file_path)

    if config_file:
        config_file_path = Path(config_file)
    else:
        config_file_path = env_folder_path / Path(DEFAULT_CONFIG_FILE)

    if modules_file:
        module_file_path = Path(modules_file)
    else:
        module_file_path = env_folder_path / Path(DEFAULT_MODULES_FILE)

    # Add all global values in the context
    ctx.obj["env_folder_path"] = env_folder_path
    ctx.obj["src_folder_path"] = src_folder_path
    ctx.obj["filestore_folder_path"] = filestore_folder_path
    ctx.obj["script_folder_path"] = script_folder_path
    ctx.obj["log_folder_path"] = log_folder_path
    ctx.obj["log_prefix"] = log_prefix
    ctx.obj["config_file_path"] = config_file_path
    ctx.obj["module_file_path"] = module_file_path

    # Load the main configuration file
    if config_file_path.exists():
        with open(config_file_path) as file:
            config = yaml.safe_load(file)
            ctx.obj["config"] = config
    elif ctx.invoked_subcommand != "init":
        raise


main.add_command(copydb)
main.add_command(restoredb)
main.add_command(docker_build)
main.add_command(dropdb)
main.add_command(dumpdb)
main.add_command(estimate_workload)
main.add_command(execute_script_python)
main.add_command(execute_script_sql)
main.add_command(generate_module_analysis)
main.add_command(get_code)
main.add_command(init)
main.add_command(install_from_csv)
main.add_command(psql)
main.add_command(pull_submodule)
main.add_command(run)
main.add_command(upgrade)
