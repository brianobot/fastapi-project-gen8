import os
import re
import time

import argparse
import subprocess
import importlib.metadata

from typing import cast
from pathlib import Path

from .helpers import (
    slugify,
    error_print,
    success_print,
    warning_print,
    clone_repository,
    display_intro_text,
)


def generate_default_project_details() -> dict[str, str | int | tuple]:
    """
    Generates Default Project Details

    For Single Value Constant Details like name, description etc
    The values are provided to the dictionary as simple String values
    But for Enumerated Values like open_source_license type
    the options are passed as a list of tuples where the the first item in tuple
    if the enumerate for the item and the second item is the actual value to be stored,

    like so

    open_source_license: (
        "<default_enumeration>", [
            (<enumeration>, "<actual_value>"),
            ...
        ]
    )

    """
    return {
        "name": "My Awesome FastAPI Project",
        "slug_name": "my_awesome_fastapi_project",
        "description": "FastAPI Project Description",
        "author(s)": "John Doe",
        "virtual_env_folder_name": "venv",
        "version": "0.1.0",
        "email": "brianobot9@gmail.com",
        "repository_link": "",
        "open_source_license": (
            1,
            [
                "MIT",
                "BSD",
                "GPLv3",
                "Apache Software License 2.0",
                "Not open source",
            ],
        ),
    }


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


def get_project_detail(
    attr: str,
    default: str | tuple[int, list[str]],
    project_detail: dict[str, str | int | tuple],
) -> str | int:
    """
    Get a project detail (attr) from the user via the command line interface, if nothing is provided
    the default value is used for the project detail value.
    """

    if "_" in attr:
        attr = attr.lower()

    if attr == "slug_name":
        default = slugify(str(project_detail["name"]))

    # Tuples Attrs means the detail have options, so process them differently
    if not isinstance(default, tuple):
        detail = input(f"Enter Project {attr} ['{default}']: ")
    else:
        count = 0
        detail = ""
        is_not_valid = True

        default_value = ProjectOptionConfig.get_default_option(default)

        while is_not_valid:
            options = default[1]
            print("Options: ", options)

            print(f"Select {attr}:")
            for index, option in enumerate(options, start=1):
                print(f"\t{index} - {option}")

            prompt_msg = f"Choose from {', '.join(str(i) for i in range(1, index + 1))}: [{cast(tuple, project_detail[attr])[0]}]: "
            detail_index = input(prompt_msg)

            if not detail_index or detail_index.isspace():
                detail = default_value
                is_not_valid = False
            elif not detail_index.isdigit():
                warning_print(
                    f"Invalid Value {detail_index} for {attr}... Please Try Again!"
                )
            elif int(detail_index) not in range(1, index + 1):
                warning_print(
                    f"Invalid Value {detail_index} for {attr}... Please Try Again!"
                )
            else:
                detail = ProjectOptionConfig.get_option_at(options, int(detail_index))
                is_not_valid = False

            count += 1
            if count > 3:
                break

        if count >= 3:
            error_print(f"Failed Due to repeated (X3) Invalid Value for {attr}")
            exit(1)

    # Process the value provided by the user
    if attr == "slug_name":
        detail = slugify(cast(str, detail)) if detail else None
    if attr == "authors":
        detail = tuple(cast(str, detail).split(","))
    return detail if detail else default


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
    # Clone The Default Project Template into Folder with Project Slug Name
    # check if the project already exist

    project_slug_name = project_detail["slug_name"]
    if Path(project_slug_name).exists():
        error_print("Directory Already Exist")
        exit(1)

    clone_repository(
        "https://github.com/brianobot/fastAPI_project_structure", project_slug_name
    )

    # Move into the Project Directory and Setup Git
    os.chdir(project_slug_name)

    # Create the Log directory
    subprocess.Popen(["mkdir", "logs"])

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
    subprocess.Popen(["git", "pull", "origin", "user-with-email", "--no-edit"]).wait()

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
    project_details = generate_default_project_details()

    start_time = (
        time.time()
    )  # this is an internal metric to track the duration for each project generation
    for attr, default_value in project_details.items():
        detail = get_project_detail(attr.title(), default_value, project_details)
        project_details[
            attr
        ] = detail  # update the default project detail with the provided one
        success_print(f"Project {attr.title()} = {detail}")

    elapsed_time = time.time() - start_time
    print("----------------------------------------------")
    success_print(f"Elasped Time: {elapsed_time:.4f} secs 🎉🎉")
    print("----------------------------------------------")

    # Generate Projects with the Details Provided by the User
    generate_project_scaffold(cast(dict[str, str], project_details))


if __name__ == "__main__":
    main()
