import argparse
import importlib.metadata
import os
import re
import subprocess
import time
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
)

"""
Step 1:
    init the script
    > fastapi-gen8

Step 2
    for each project detail prompt the user for an input, use fallback on empty inputs
    > Enter Project Name ['My Awesome FastAPI Project']:

Step 3
    Clone the Standard FastAPI project from Github alias the directory name as the slug_name provided by user
    Change Directory into the newly cloned directory
    Apply Book Keeping Changes
        - Create logs/ directory
        - Replace placeholders e.g `{project_name}` values across project files with user provided details
        - Remove Former git metadata
        - Initialize git on the directory again
        - Add origin provided by the user
        - Create Python Virtual Environment
        - Install Packages in activated virtual environment

"""


class ProjectOptionConfig:
    """
    Utility Functions for working with Project Detail Options.
    """

    @classmethod
    def get_option_at(cls, option: list[str], position: int) -> str:
        """
        Since indexes are zero based and position are 1 based
        substracting 1 from each get the option at the current index
        """
        return option[position - 1]

    @classmethod
    def get_default_option(cls, default: tuple[int, list[str]]) -> str:
        """
        Takes the whole default value, extracts the default index and extract the default value
        based on the default index
        """
        default_index = default[0]
        return cls.get_option_at(default[1], default_index)


def apply_project_metadata(project_detail: dict[str, str]) -> None:
    # replace placeholder values with user generated values
    target = Path("app/main.py")
    if not target.exists():
        print("main.py not found, skipping metadata update")
        return

    content = target.read_text()

    content = content.replace(
        'title="{{ project_name }}"',
        f'title="{project_detail["name"]}"',
        1,
    )
    content = content.replace(
        'version="{{ project_version }}"',
        f'version="{project_detail["version"]}"',
        1,
    )

    content = re.sub(
        r'summary\s*=\s*["\']\{\{\s*project_description\s*\}\}["\']',
        f'summary="{project_detail["description"]}"',
        content,
        count=1,
    )
    target.write_text(content)


def generate_project_scaffold(project_detail: dict[str, str]):
    project_slug = project_detail["slug"]
    if Path(project_slug).exists():
        error_print("Directory Already Exist")
        exit(1)

    clone_template_repository(project_slug)

    # Move into the Project Directory and Setup Git
    os.chdir(project_slug)

    # Create the logs directory
    Path("logs").mkdir(exist_ok=True)

    # change default project values to user-defined values
    apply_project_metadata(
        cast(
            dict[str, str],
            {
                "name": str(project_detail["name"]),
                "description": str([project_detail["description"]]),
                "version": str(project_detail["version"]),
            },
        )
    )
    # Commit changes for metadata changes before continueing
    subprocess.Popen(["git", "commit", "-am", "Save Metadata Changes"]).wait()
    # pull changes from the user-with-email branch
    subprocess.Popen(["git", "config", "pull.rebase", "false"]).wait()
    # Remove former git metadata and link repo to the provided repo link
    subprocess.Popen(["rm", "-rf", ".git"]).wait()
    subprocess.Popen(["git", "init"]).wait()
    subprocess.Popen(
        ["git", "remote", "add", "origin", project_detail["repository_link"]]
    ).wait()

    # create and activate virtual environment
    subprocess.Popen(["python3", "-m", "venv", "venv"]).wait()
    subprocess.Popen(
        ["bash", "-c", "source venv/bin/activate && pip install -r requirements.txt"]
    ).wait()

    print("____________________________________________")
    success_print("✅ Completed Project Initialization 🚀")
    print("____________________________________________")


def prompt_user_for_input(
    attribute: str, default_value: Any, project_details: dict[str, Any]
):
    if attribute == "slug":
        default_value = slugify(project_details.get("name", default_value))

    if attribute == "description":
        project_name = project_details["name"]
        default_value = f"Official API for {project_name}"

    if attribute == "open_source_license":
        default_index = default_value[0]
        options = default_value[1]

    prompt = f"Enter Project's {attribute} [{default_value}]: "
    user_input = input(prompt)

    if attribute == "open_source_license":
        if user_input not in range(1, 6):
            warning_print("Invalid Input for Index. Default to MIT LICENSE")
            return options[default_index - 1]  # type: ignore
        else:
            return options[int(user_input) - 1]  # type: ignore

    return user_input if user_input else default_value


def main():
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
    success_print(f"Elasped Time: {elapsed_time:.4f} secs 🎉🎉")
    print("----------------------------------------------")

    # Generate Projects with the Details Provided by the User
    generate_project_scaffold(project_details)


if __name__ == "__main__":
    main()
