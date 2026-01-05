import pytest
import unittest.mock

from typing import cast
from fastapi_gen8 import main


def test_display_intro_text(capsys):
    main.display_intro_text()
    
    captured = capsys.readouterr()
    assert main.display_intro_text.__doc__
    assert isinstance(captured.out, str)
    assert captured.err == ""
    
    
def test_generate_default_project_details():
    result = main.generate_default_project_details()
    assert main.generate_default_project_details.__doc__
    assert isinstance(result, dict)
    assert all(isinstance(default_value, str | int | tuple) for default_value in result.values())
    

@pytest.mark.parametrize(
    "attr,default_value,project_detail",
    [
        ("name", "My Awesome FastAPI Project Test", main.generate_default_project_details()),
        ("slug_name", "my_awesome_fastapi_project", main.generate_default_project_details()),
        ("description", "FastAPI Project Description", main.generate_default_project_details()),
        ("author(s)", "John Doe", main.generate_default_project_details()),
        ("virtual_env_folder_name", "venv", main.generate_default_project_details()),
        ("version", "0.0.1", main.generate_default_project_details()),
        ("email", "brianobot9@gmail.com", main.generate_default_project_details()),
        ("repository_url", "Default Name", main.generate_default_project_details()),
        ("open_source_license", (1, [
            "MIT", 
            "BSD", 
            "GPLv3", 
            "Apache Software License 2.0", 
            "Not open source",
        ]), main.generate_default_project_details()),
    ]
)
def test_get_project_detail(attr: str, default_value: str | int | tuple, project_detail: dict[str, str | int | tuple]):
    with unittest.mock.patch('builtins.input', side_effect=[None]):
        result = main.get_project_detail(attr, default_value, project_detail)
        print("✅ Response: ", result)
        # assert None
        if isinstance(default_value, tuple):
            default_value = cast(tuple, default_value)
            assert result == cast(list, default_value[1])[default_value[0] - 1]
        else:
            assert result == default_value
        assert isinstance(result, str | int | tuple)

