# Default value presented for each project detail during the interactive prompt.
#
# Most values are plain strings. ``open_source_license`` is the exception: it is
# a ``(default_index, options)`` tuple, where ``default_index`` is the 1-based
# position of the option chosen when the user gives no (or an invalid) input.
#
# ``authors``, ``email`` and ``virtual_env_folder_name`` are collected from the
# user but not yet applied to the generated project (reserved for future use).
DEFAULT_PROJECT_DETAIL = {
    "name": "Awesome FastAPI Project",
    "slug": "awesome_fastapi_project",
    "description": "Official API for Awesome FastAPI Project",
    "authors": "John Doe",
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
