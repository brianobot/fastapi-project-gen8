import unittest.mock
from typing import cast

import pytest

from src.fastapi_gen8 import main


def test_display_intro_text(capsys):
    main.display_intro_text()

    captured = capsys.readouterr()
    assert main.display_intro_text.__doc__
    assert isinstance(captured.out, str)
    assert captured.err == ""


@pytest.mark.parametrize(
    "attr,default_value,project_detail",
    [
        (
            "name",
            "My Awesome FastAPI Project Test",
            main.DEFAULT_PROJECT_DETAIL,
        ),
        (
            "slug_name",
            "my_awesome_fastapi_project",
            main.DEFAULT_PROJECT_DETAIL,
        ),
        (
            "description",
            "FastAPI Project Description",
            main.DEFAULT_PROJECT_DETAIL,
        ),
        ("author(s)", "John Doe", main.DEFAULT_PROJECT_DETAIL),
        ("virtual_env_folder_name", "venv", main.DEFAULT_PROJECT_DETAIL),
        ("version", "0.0.1", main.DEFAULT_PROJECT_DETAIL),
        ("email", "brianobot9@gmail.com", main.DEFAULT_PROJECT_DETAIL),
        ("repository_url", "Default Name", main.DEFAULT_PROJECT_DETAIL),
        (
            "open_source_license",
            (
                1,
                [
                    "MIT",
                    "BSD",
                    "GPLv3",
                    "Apache Software License 2.0",
                    "Not open source",
                ],
            ),
            main.DEFAULT_PROJECT_DETAIL,
        ),
    ],
)
def test_get_project_detail(
    attr: str,
    default_value: str | int | tuple,
    project_detail: dict[str, str | int | tuple],
):
    with unittest.mock.patch("builtins.input", side_effect=[None]):
        result = main.prompt_user_for_input(attr, default_value, project_detail)
        print("✅ Response: ", result)
        # assert None
        if isinstance(default_value, tuple):
            default_value = cast(tuple, default_value)
            assert result == cast(list, default_value[1])[default_value[0] - 1]
        else:
            assert result == default_value
        assert isinstance(result, str | int | tuple)
