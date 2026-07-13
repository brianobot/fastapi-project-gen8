"""FastAPI Gen8 command-line project generator.

The generation flow is:

1. Initialise the CLI (``fastapi-gen8``).
2. Prompt the user for each project detail, falling back to defaults on empty
   input.
3. Scaffold the project: clone the standard FastAPI template (renaming the
   directory to the slug), change into it, then apply bookkeeping changes —
   create ``logs/``, replace ``{{ placeholder }}`` values with the user's
   details, reset git history and re-initialise, add the user's remote, create a
   virtual environment, and install requirements.
"""

import argparse
import importlib.metadata
import os
import re
import subprocess
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from .defaults import DEFAULT_PROJECT_DETAIL
from .helpers import (
    clone_template_repository,
    display_intro_text,
    error_print,
    slugify,
    success_print,
    warning_print,
    write_license_file,
)

# Jinja-style placeholders embedded throughout the template, each mapped to the
# project detail that fills it.
PROJECT_PLACEHOLDERS = {
    "project_name": "name",
    "project_version": "version",
    "project_description": "description",
}


def _literal_repl(value: str) -> Callable[[re.Match[str]], str]:
    """A re.sub replacement that inserts ``value`` verbatim (ignoring backrefs)."""
    return lambda _match: value


def apply_project_metadata(project_detail: dict[str, str]) -> None:
    """
    Replace the ``{{ project_name }}``, ``{{ project_version }}`` and
    ``{{ project_description }}`` placeholders with the user's values across
    every text file in the generated project — not just ``app/main.py`` (the
    template also references them elsewhere, e.g. ``app/services/auth.py``).

    Whitespace inside a placeholder is tolerated, values are inserted literally,
    and binary/unreadable files (and the ``.git`` directory) are skipped.
    """
    patterns = [
        (re.compile(rf"\{{\{{\s*{placeholder}\s*\}}\}}"), project_detail[detail_key])
        for placeholder, detail_key in PROJECT_PLACEHOLDERS.items()
    ]

    for path in sorted(Path(".").rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # skip binary / unreadable files

        updated = content
        for regex, value in patterns:
            updated = regex.sub(_literal_repl(value), updated)

        if updated != content:
            path.write_text(updated, encoding="utf-8")


def run_command(cmd: list[str]) -> None:
    """
    Run an external command, raising subprocess.CalledProcessError if it fails
    so that scaffold errors surface instead of being silently swallowed.
    """
    subprocess.run(cmd, check=True)


def generate_project_scaffold(project_detail: dict[str, str]) -> None:
    project_slug = project_detail["slug"]
    if Path(project_slug).exists():
        error_print("Directory already exists")
        exit(1)

    clone_template_repository(project_slug)

    # Move into the Project Directory and Setup Git
    os.chdir(project_slug)

    # Create the logs directory
    Path("logs").mkdir(exist_ok=True)

    # Drop the template's git history and start a fresh repository so the
    # metadata commit below becomes the project's first real commit.
    run_command(["rm", "-rf", ".git"])
    run_command(["git", "init"])

    # change default project values to user-defined values
    apply_project_metadata(
        cast(
            dict[str, str],
            {
                "name": str(project_detail["name"]),
                "description": str(project_detail["description"]),
                "version": str(project_detail["version"]),
            },
        )
    )

    # Write the LICENSE file matching the user's selected license
    write_license_file(project_detail["open_source_license"], project_detail["authors"])

    # Commit the metadata changes on the fresh repository. A missing local git
    # identity shouldn't abort the whole scaffold, so this step only warns.
    run_command(["git", "add", "-A"])
    try:
        run_command(["git", "commit", "-m", "Save Metadata Changes"])
    except subprocess.CalledProcessError:
        warning_print("Could not create initial commit; skipping.")

    # Link the repo to the remote origin provided by the user, when present
    repository_link = project_detail["repository_link"]
    if repository_link:
        run_command(["git", "remote", "add", "origin", repository_link])
    else:
        warning_print(
            "No repository link provided. Add a remote manually with "
            "`git remote add origin <url>`."
        )

    # create and activate virtual environment
    run_command(["python3", "-m", "venv", "venv"])
    run_command(
        ["bash", "-c", "source venv/bin/activate && pip install -r requirements.txt"]
    )

    print("____________________________________________")
    success_print("✅ Completed Project Initialization 🚀")
    print("____________________________________________")


def prompt_user_for_input(
    attribute: str, default_value: Any, project_details: dict[str, Any]
) -> str:
    if attribute == "slug":
        default_value = slugify(project_details.get("name", default_value))

    if attribute == "description":
        project_name = project_details["name"]
        default_value = f"Official API for {project_name}"

    prompt = f"Enter Project's {attribute} [{default_value}]: "
    user_input = input(prompt)

    if attribute == "open_source_license":
        # default_value is a (default_index, options) tuple; both are 1-based.
        default_index, options = default_value
        if (
            not user_input
            or not user_input.isdigit()
            or int(user_input) not in range(1, len(options) + 1)
        ):
            warning_print("Invalid Input for Index. Default to MIT LICENSE")
            return options[default_index - 1]
        return options[int(user_input) - 1]

    return user_input if user_input else default_value


def main() -> None:
    """
    Main entry point to interacting with the Command Line Utility of the Generator Library
    """
    parser = argparse.ArgumentParser(
        prog="fastapi-gen8",
        description="Generate clean, production-ready FastAPI project scaffolds",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {importlib.metadata.version('fastapi-gen8')}",
    )

    _args = parser.parse_args()

    display_intro_text()
    project_details = DEFAULT_PROJECT_DETAIL.copy()

    # this is an internal metric to track the duration for each project generation
    start_time = time.time()

    for attribute, default_value in project_details.items():
        detail = prompt_user_for_input(attribute, default_value, project_details)
        project_details[attribute] = detail
        success_print(f"Project {attribute.title()} = {detail}")

    elapsed_time = time.time() - start_time
    print("----------------------------------------------")
    success_print(f"Elapsed Time: {elapsed_time:.4f} secs 🎉🎉")
    print("----------------------------------------------")

    # Generate Projects with the Details Provided by the User. By this point
    # every prompted value has been resolved to a string.
    generate_project_scaffold(cast(dict[str, str], project_details))


if __name__ == "__main__":
    main()
