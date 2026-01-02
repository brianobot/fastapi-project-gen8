
from fastapi_gen8.helpers import slugify, success_print, warning_print, error_print


def test_slugify():
    assert slugify("SingleWord") == "singleword"
    assert slugify("Double Word") == "double_word"
    assert slugify("Word-With-Dash") == "word_with_dash"
    
def test_success_print(capsys):
    success_print("Success")
    assert capsys.readouterr().out == "\033[92mSuccess\033[00m\n"
    
def test_warning_print(capsys):
    warning_print("Warning")
    assert capsys.readouterr().out == "\033[33mWarning\033[00m\n"
    
def test_error_print(capsys):
    error_print("Error")
    assert capsys.readouterr().out == "\033[31mError\033[00m\n"