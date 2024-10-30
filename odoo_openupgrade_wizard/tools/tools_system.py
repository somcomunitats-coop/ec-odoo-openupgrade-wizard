import argparse
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import importlib_resources
from git_aggregator import main as gitaggregate_cmd
from git_aggregator.utils import working_directory_keeper
from jinja2 import Template
from loguru import logger
from plumbum.cmd import chmod, mkdir
from plumbum.commands.processes import ProcessExecutionError


def get_script_folder(ctx, migration_step: dict) -> Path:
    return ctx.obj["script_folder_path"] / migration_step["complete_name"]


def ensure_folder_writable(folder_path: Path):
    logger.info(f"Make writable the folder '{folder_path}'")
    try:
        chmod(["--silent", "--recursive", "o+w", str(folder_path)])
    except ProcessExecutionError:
        pass


def ensure_folder_exists(
    folder_path: Path, mode: str = "755", git_ignore_content: bool = False
):
    """Create a local folder.
    - directory is created if it doesn't exist.
    - mode is applied if defined.
    - a log is done at INFO level.
    """
    if not folder_path.exists():
        cmd = ["--parents", folder_path]
        cmd = ["--mode", mode] + cmd
        logger.info(f"Creating folder '{folder_path}' ...")
        mkdir(cmd)

    if git_ignore_content:
        ensure_file_exists_from_template(
            folder_path / Path(".gitignore"),
            ".gitignore.j2",
        )


def ensure_file_exists_from_template(
    file_path: Path, template_name: str, **args
):
    template_folder = (
        importlib_resources.files("odoo_openupgrade_wizard") / "templates"
    )
    template_path = template_folder / template_name
    if not template_path.exists():
        logger.warning(
            f"Unable to generate {file_path},"
            f" the template {template_name} has not been found."
            f" If it's a Dockerfile,"
            f" you should maybe contribute to that project ;-)"
        )
        return
    text = template_path.read_text()
    template = Template(text)
    output = template.render(args)

    if file_path.exists():
        # Check if content is different
        with open(file_path, "r") as file:
            data = file.read()
            file.close()
            if data == output:
                return

        log_text = f"Updating file '{file_path}' from template ..."
    else:
        log_text = f"Creating file '{file_path}' from template ..."

    with open(file_path, "w") as f:
        logger.info(log_text)
        print(output, file=f)


def git_aggregate(folder_path: Path, config_path: Path, jobs: int):
    args = argparse.Namespace(
        command="aggregate",
        config=str(config_path),
        jobs=jobs,
        dirmatch=None,
        do_push=False,
        expand_env=False,
        env_file=None,
        force=True,
    )
    with working_directory_keeper:
        os.chdir(folder_path)
        logger.info(
            f"Gitaggregate source code for {config_path}."
            " This can take a while ..."
        )
        gitaggregate_cmd.run(args)


def get_local_user_id():
    return os.getuid()


def execute_check_output(args_list, working_directory=None):
    logger.debug(f"Execute {' '.join(args_list)}")
    subprocess.check_output(args_list, cwd=working_directory)


def dump_filestore(
    ctx,
    database: str,
    destpath: os.PathLike,
    copyformat: str = "d",
):
    """Copy filestore of database to destpath using copyformat.
    copyformat can be 'd' for directory, a normal copy, or 't' for a
    copy into a tar achive, or 'tgz' to copy to a compressed tar file.
    """
    valid_format = ("d", "t", "tgz", "txz")
    if copyformat not in valid_format:
        raise ValueError(
            f"copyformat should be one of the following {valid_format}"
        )

    filestore_folder_path = ctx.obj["env_folder_path"] / "filestore/filestore"
    filestore_path = filestore_folder_path / database

    if copyformat == "d":
        shutil.copytree(filestore_path, destpath)

    elif copyformat.startswith("t"):
        wmode = "w"
        if copyformat.endswith("gz"):
            wmode += ":gz"
        elif copyformat.endswith("xz"):
            wmode += ":xz"

        with tarfile.open(destpath, wmode) as tar:
            tar.add(filestore_path, arcname="filestore")


def restore_filestore(
    ctx,
    database: str,
    src_path: Path,
    file_format: str = "d",
):
    """Restore filestore of database from src_path using file_format.
    file_format can be :
        'd' for 'directory': a normal copy,
        't' / 'tgz' for 'tar': an extraction from a tar achive
    """
    valid_format = ("d", "t", "tgz")
    if file_format not in valid_format:
        raise ValueError(
            f"file_format should be one of the following {valid_format}"
        )

    filestore_path = (
        ctx.obj["env_folder_path"] / "filestore/filestore" / database
    )

    logger.info(f"Restoring filestore of '{database}'...")
    if file_format == "d":
        shutil.copytree(src_path, filestore_path)

    else:  # works for "t" and "tgz"
        tar = tarfile.open(src_path)
        tar.extractall(path=filestore_path)
