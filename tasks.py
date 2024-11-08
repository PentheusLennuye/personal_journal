"""
Invoke tasks
"""

import os

from invoke import task

PROJECT_NAME = "personal_journal"
SHELL = "/bin/sh"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@task
def build(context):
    """
    Build the project Docker image. Dev will build the project
    """
    command = (
        f"docker build -t {PROJECT_NAME}_dev -f development/Dockerfile "
        f"{CURRENT_DIR}"
    )
    return context.run(command, shell=SHELL)


@task
def debug(context, env="development"):
    """Run the correct docker-compose ensuring stdout and CTRL-C access."""
    return docker_compose(context, "up", env)


def docker_compose(context, command, env, **kwargs):
    """Run a docker compose command."""
    pg_ver = get_postgres_version(context, env)
    command = (
        f"POSTGRES_VERSION={pg_ver} docker compose -p {PROJECT_NAME} "
        f"--project-directory {CURRENT_DIR} "
        f"-f {env}/docker-compose.yml {command}"
    )
    print(command)
    return context.run(command, shell=SHELL, **kwargs)


def get_postgres_version(context, env="development"):
    """Grab the postgres_version from the correct dev.env file."""
    command = f"grep POSTGRES_VER {env}/dev.env"
    return context.run(command, echo=False).stdout.split("=")[1].strip()


@task
def start(context, env="development"):
    """Run the correct docker-compose and detach."""
    return docker_compose(context, "up -d", env)


@task
def stop(context, env="development"):
    """Stop the docker run."""
    return docker_compose(context, "down", env)


@task
def destroy(context, env="development"):
    """Stop and destroy the volumes."""
    return docker_compose(context, "down --volumes", env)


@task
def restart(context, env="development"):
    """Restart the docker run."""
    return docker_compose(context, "restart", env)


@task
def cli(context, env="development", container="app", rshell="sh"):
    """Open a shell into a running container"""
    return docker_compose(context, f"exec {container} {rshell}", env, pty=True)


# ------------------------------------------------------------------------------
# FORMATTING
# ------------------------------------------------------------------------------


@task
def black(context, autoformat=False):
    """Check Python code style with Black."""
    if autoformat:
        black_command = "black"
    else:
        black_command = "black --check --diff"
    run_command(context, f"{black_command} {CURRENT_DIR}")


def run_command(context, command):
    """Run a command inside poetry."""
    return context.run(f"poetry run {command}")


@task
def flake8(context):
    """Check for PEP8 compliance and other style issues."""
    run_command(context, "flake8 .")


@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting."""
    run_command(context, f"pydocstyl {CURRENT_DIR}")
