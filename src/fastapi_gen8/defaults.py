DEFAULT_PROJECT_DETAIL = {
    "name": "Awesome FastAPI Project",
    "slug": "awesome_fastapi_project",
    "description": "Official API for Awesome FastAPI Project",
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
