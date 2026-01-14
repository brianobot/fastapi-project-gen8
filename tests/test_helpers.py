from src.fastapi_gen8 import helpers


def test_slugify():
    assert helpers.slugify("SingleWord") == "singleword"
    assert helpers.slugify("Double Word") == "double_word"
    assert helpers.slugify("Word-With-Dash") == "word_with_dash"


def test_success_print(capsys):
    helpers.success_print("Success")
    assert capsys.readouterr().out == "\033[92mSuccess\033[00m\n"


def test_warning_print(capsys):
    helpers.warning_print("Warning")
    assert capsys.readouterr().out == "\033[33mWarning\033[00m\n"


def test_error_print(capsys):
    helpers.error_print("Error")
    assert capsys.readouterr().out == "\033[31mError\033[00m\n"
