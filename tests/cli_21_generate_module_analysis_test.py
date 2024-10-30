from pathlib import Path

from odoo_openupgrade_wizard.tools.tools_odoo import get_odoo_env_path

from . import (
    build_ctx_from_config_file,
    cli_runner_invoke,
    mock_odoo_rpc_url,
    move_to_test_folder,
)


def test_cli_generate_module_analysis(mocker):
    move_to_test_folder()
    mock_odoo_rpc_url(mocker)
    ctx = build_ctx_from_config_file()

    db_name = "database_test_cli___generate_module_analysis"

    # identify main analysis file of openupgrade
    analysis_file_path = get_odoo_env_path(ctx, 15.0) / Path(
        "src/openupgrade/openupgrade_scripts/scripts"
        "/base/15.0.1.3/upgrade_general_log.txt"
    )

    # We remove this file and run the analysis
    try:
        analysis_file_path.unlink()
    except FileNotFoundError:
        pass

    analysis_file_path
    cli_runner_invoke(
        [
            "generate-module-analysis",
            "--step=2",
            f"--database={db_name}",
            "--modules=base",
        ],
    )

    # The file should has been recreated by the analysis command
    assert analysis_file_path.exists()
