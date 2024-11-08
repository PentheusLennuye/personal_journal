"""
Invoke tasks
"""

import os
import sys

import toml

from invoke import task

PROJECT_NAME = "personal_journal"
SHELL = "/bin/sh"

BAD_PYPROJECT = 1
BUILD_ERROR = 2
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@task
def build(context, env="development", repo_host=None, repo_owner=None):
    """
    Build the project Docker image. If there is no repo_host, then the docker
    image will be built and stored locally. Otherwise, the build tag will
    be {repo_host}/{repo_owner}/{project-name}:{version}.

    {version} is taken from pyproject.toml
    """
    name, version = get_project_version_or_die()
    tag = ""
    if env == "development":
        tag = f"{name}:{version}-dev"
    elif env == "staging":
        if repo_host is None or repo_owner is None:
            print("Staging needs --repo-host and --repo-owner set")
            sys.exit(BUILD_ERROR)
        tag = f"{repo_host}/{repo_owner}/{name}:{version}-rc"
    elif env == "production":
        if repo_host is None or repo_owner is None:
            print("Production needs --repo-host and --repo-owner set")
            sys.exit(BUILD_ERROR)
        tag = f"{repo_host}/{repo_owner}/{name}:{version}"
    else:
        print("Environment {env} does not have a rule for docker build")
        sys.exit(BUILD_ERROR)

    command = (
        f"docker build -t {tag} -f {env}/Dockerfile {CURRENT_DIR}"
    )
    print(command)
    return run_command(context, command)


def get_project_version_or_die():
    """Read the pyproject.toml file to get the project version."""
    data = toml.load(f"{CURRENT_DIR}/pyproject.toml")
    ok, msg = is_pyproject_sane(data)
    if not ok:
        print(msg)
        sys.exit(BAD_PYPROJECT)
    return data["tool"]["poetry"]["name"], data["tool"]["poetry"]["version"]


def is_pyproject_sane(data):
    """Check pyproject for correctness."""
    if "tool" not in data:
        return False, "pyproject does not have [tool.poetry] entry"
    if "poetry" not in data["tool"]:
        return False, "pyproject does not have [tool.poetry] entry"
    if "version" not in data["tool"]["poetry"]:
        return False, "pyproject does not have 'version' in [tool.poetry]"
    if "version" not in data["tool"]["poetry"]:
        return False, "pyproject does not have 'version' in [tool.poetry]"
    return True


def run_command(context, command):
    """Run a command inside poetry."""
    return context.run(command)


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


@task
def flake8(context):
    """Check for PEP8 compliance and other style issues."""
    run_command(context, "flake8 .")


@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting."""
    run_command(context, f"pydocstyl {CURRENT_DIR}")


# ---------------------------------------------------------------------------
# Accuracy and fitness for purpose
# ---------------------------------------------------------------------------


@task
def unittest(context):
    """Perform unit tests."""
    # command = "python /opt/netbox/netbox/manage.py test scripts"
    # run_command(context, command)
    run_command(context, f"python -m pytest {CURRENT_DIR}")


@task
def coverage(context):
    """Ensure excellent unit test coverage."""
    run_command(context, f"python -m pytest --cov={CURRENT_DIR} tests/")


@task
def lint(context):
    """Perform linting checks."""
    print("Black linting")
    black(context)
    print("Flake8 linting")
    flake8(context)
    print("Pydocstyle linting")
    pydocstyle(context)
