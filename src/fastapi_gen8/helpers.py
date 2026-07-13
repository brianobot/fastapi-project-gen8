import datetime
import subprocess
from pathlib import Path

# Bundled license templates, keyed by the option label shown to the user in
# defaults.DEFAULT_PROJECT_DETAIL. "Not open source" has no template — it falls
# back to a short proprietary notice in write_license_file().
LICENSE_DIR = Path(__file__).resolve().parent / "licenses"
LICENSE_TEMPLATES = {
    "MIT": "mit.txt",
    "BSD": "bsd-3-clause.txt",
    "GPLv3": "gpl-3.0.txt",
    "Apache Software License 2.0": "apache-2.0.txt",
}


def write_license_file(license_choice: str, author: str) -> None:
    """
    Write a LICENSE file into the current directory for the chosen license.

    MIT/BSD templates carry ``[year]``/``[fullname]`` placeholders that are
    filled with the current year and the author. Apache-2.0/GPLv3 are written
    verbatim (their copyright notice lives in source headers, not the license
    body). Any unrecognised choice (e.g. "Not open source") writes a short
    proprietary "all rights reserved" notice instead.
    """
    year = str(datetime.date.today().year)
    template = LICENSE_TEMPLATES.get(license_choice)

    if template is None:
        Path("LICENSE").write_text(
            f"Copyright (c) {year} {author}\nAll rights reserved.\n"
        )
        return

    text = (LICENSE_DIR / template).read_text(encoding="utf-8")
    text = text.replace("[year]", year).replace("[fullname]", author)
    Path("LICENSE").write_text(text)


def display_intro_text() -> None:
    """
    Displays the Introduction Text of the Library as a Nice and Friendly UI
    Alongside a short instructions on how to use the library for new users.
    """
    intro_message = """
    ______________________________________________________________

    ███████╗ █████╗ ███████╗████████╗ █████╗ ██████╗ ██╗
    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║
    █████╗  ███████║███████╗   ██║   ███████║██████╔╝██║
    ██╔══╝  ██╔══██║╚════██║   ██║   ██╔══██║██      ██║
    ██║     ██║  ██║███████║   ██║   ██║  ██║██║    ║██║
    ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝    ╚╝╚╝

    ██████╗ ██████╗  ██████╗ ███████╗███████╗ ██████  ████████╗
    ██╔══██╗██╔══██╗██╔═══██╗ ════██╗██╔════╝██╔════╝ ╚══██╔══╝
    ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║         ██║
    ██╔═══╝ ██╔══██╗██║   ██║███  ██║██╔══╝  ██║         ██║
    ██║     ██║  ██║╚██████╔╝██████╔╝███████╗╚██████╗    ██║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝

     ██████╗ ███████╗███╗   ██╗ █████╗
    ██╔════╝ ██╔════╝████╗  ██║██╔══██╗
    ██║  ███╗█████╗  ██╔██╗ ██║ █████╔╝
    ██║   ██║██╔══╝  ██║╚██╗██║██╔══██╗
    ╚██████╔╝███████╗██║ ╚████║ █████╔╝
        ╚═════╝ ╚══════╝╚═╝  ╚╝ ╚════╝
    ______________________________________________________________
    """
    print(intro_message)
    description = """
    Generate a fully structured FastAPI projects instantly.
    Boilerplate code, ready-to-run endpoints, and project scaffolding
    all in one simple command. Kickstart your backend in seconds!

    Provide Project Details to each prompt and press 'Enter' to complete project setup

    NOTES: Values placed within square brackets ([My Awesome FastAPI Project]) are defaults values for the project details
    If you do not provide a value for any particular, those values are used instead.

    Have a Blast 🚀 - Brian
    _____________________________________________________________________________________________________
    """
    # FUN 🚀

    # How Fast Can you Complete your FastAPI project setup?
    # Blaze through the steps to make the global leaderboard for projects generated with FastAPI Project Gen8.
    # In Order to qualify for this leaderboard, you have to make sure to input every project detail and not use defaults
    # even though the defaults match your project attribute.
    # Current Best Record: {get_current_best_record()[0]} seconds - Title: [{get_current_best_record()[1]}]
    print(description)


def slugify(text: str) -> str:
    return text.replace(" ", "_").replace("-", "_").lower()


def success_print(value: str):
    print("\033[92m{}\033[00m".format(value))


def warning_print(value: str):
    print("\033[33m{}\033[00m".format(value))


def error_print(value: str):
    print("\033[31m{}\033[00m".format(value))


def clone_template_repository(
    dir_name: str,
    repository_url="https://github.com/brianobot/fastAPI_project_structure",
):
    try:
        subprocess.run(["git", "clone", repository_url, dir_name], check=True)
    except subprocess.CalledProcessError as err:
        error_print(f"Failed to Clone Template Repo: Reason: {err}")
        exit(1)
