import datetime
import subprocess

import pytest

from fastapi_gen8 import helpers

# --- slugify ---------------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected",
    [
        ("SingleWord", "singleword"),
        ("Double Word", "double_word"),
        ("Word-With-Dash", "word_with_dash"),
        ("My Awesome-Project", "my_awesome_project"),
    ],
)
def test_slugify(text, expected):
    assert helpers.slugify(text) == expected


# --- colour printers -------------------------------------------------------


@pytest.mark.parametrize(
    "printer, ansi_code",
    [
        (helpers.success_print, "\033[92m"),
        (helpers.warning_print, "\033[33m"),
        (helpers.error_print, "\033[31m"),
    ],
)
def test_color_printers_wrap_text_in_ansi_codes(capsys, printer, ansi_code):
    printer("Message")
    assert capsys.readouterr().out == f"{ansi_code}Message\033[00m\n"


# --- display_intro_text ----------------------------------------------------


def test_display_intro_text_prints_to_stdout_only(capsys):
    helpers.display_intro_text()
    captured = capsys.readouterr()
    assert captured.out  # a banner was printed
    assert captured.err == ""


# --- clone_template_repository ---------------------------------------------


def test_clone_template_repository_clones_default_repo(monkeypatch):
    calls = []
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: calls.append(cmd))

    helpers.clone_template_repository("my_project")

    assert calls == [
        [
            "git",
            "clone",
            "https://github.com/brianobot/fastAPI_project_structure",
            "my_project",
        ]
    ]


def test_clone_template_repository_accepts_custom_url(monkeypatch):
    calls = []
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: calls.append(cmd))

    helpers.clone_template_repository("proj", repository_url="https://example.com/x")

    assert calls[0] == ["git", "clone", "https://example.com/x", "proj"]


def test_clone_template_repository_exits_on_failure(monkeypatch, capsys):
    def failing_run(cmd, **kwargs):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", failing_run)

    with pytest.raises(SystemExit) as exit_info:
        helpers.clone_template_repository("proj")

    assert exit_info.value.code == 1
    assert "Failed to Clone Template Repo" in capsys.readouterr().out


# --- write_license_file ----------------------------------------------------


def test_write_license_file_fills_mit_placeholders(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    helpers.write_license_file("MIT", "Ada Lovelace")

    text = (tmp_path / "LICENSE").read_text()
    assert text.startswith("MIT License")
    assert "Ada Lovelace" in text
    assert str(datetime.date.today().year) in text
    # every placeholder must be substituted
    assert "[year]" not in text
    assert "[fullname]" not in text


def test_write_license_file_writes_verbatim_for_apache(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    helpers.write_license_file("Apache Software License 2.0", "Ada Lovelace")

    text = (tmp_path / "LICENSE").read_text()
    assert "Apache License" in text
    assert "Version 2.0" in text


def test_write_license_file_writes_verbatim_for_gplv3(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    helpers.write_license_file("GPLv3", "Ada Lovelace")

    text = (tmp_path / "LICENSE").read_text()
    assert "GNU GENERAL PUBLIC LICENSE" in text


def test_write_license_file_uses_proprietary_notice_for_unknown_choice(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)

    helpers.write_license_file("Not open source", "Ada Lovelace")

    text = (tmp_path / "LICENSE").read_text()
    assert "All rights reserved." in text
    assert "Ada Lovelace" in text
