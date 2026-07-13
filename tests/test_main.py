import subprocess

import pytest

from fastapi_gen8 import main

LICENSE_DEFAULT = main.DEFAULT_PROJECT_DETAIL["open_source_license"]


def mock_input(monkeypatch, value):
    """Make builtins.input return `value` for the next prompt."""
    monkeypatch.setattr("builtins.input", lambda prompt="": value)


# --- prompt_user_for_input -------------------------------------------------


def test_prompt_returns_user_input_when_provided(monkeypatch):
    mock_input(monkeypatch, "My Project")
    assert main.prompt_user_for_input("name", "Default", {}) == "My Project"


def test_prompt_falls_back_to_default_on_empty_input(monkeypatch):
    mock_input(monkeypatch, "")
    assert main.prompt_user_for_input("name", "Default", {}) == "Default"


def test_prompt_slug_is_derived_from_project_name(monkeypatch):
    mock_input(monkeypatch, "")
    result = main.prompt_user_for_input("slug", "ignored", {"name": "My Cool App"})
    assert result == "my_cool_app"


def test_prompt_description_is_templated_from_project_name(monkeypatch):
    mock_input(monkeypatch, "")
    result = main.prompt_user_for_input("description", "ignored", {"name": "Ledger"})
    assert result == "Official API for Ledger"


def test_prompt_license_valid_selection_returns_chosen_option(monkeypatch):
    mock_input(monkeypatch, "3")
    result = main.prompt_user_for_input("open_source_license", LICENSE_DEFAULT, {})
    assert result == "GPLv3"


@pytest.mark.parametrize("bad_input", ["", "0", "6", "99", "abc", "-1", " "])
def test_prompt_license_invalid_input_defaults_to_mit(monkeypatch, capsys, bad_input):
    mock_input(monkeypatch, bad_input)
    result = main.prompt_user_for_input("open_source_license", LICENSE_DEFAULT, {})
    assert result == "MIT"
    assert "Invalid Input" in capsys.readouterr().out


# --- apply_project_metadata ------------------------------------------------


def write_template(tmp_path, body):
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    target = app_dir / "main.py"
    target.write_text(body)
    return target


def test_apply_metadata_replaces_every_placeholder(tmp_path, monkeypatch):
    target = write_template(
        tmp_path,
        "FastAPI(\n"
        '    title="{{ project_name }}",\n'
        '    version="{{ project_version }}",\n'
        '    summary="{{ project_description }}",\n'
        ")\n",
    )
    monkeypatch.chdir(tmp_path)

    main.apply_project_metadata(
        {"name": "Cool API", "version": "1.2.3", "description": "Does things"}
    )

    content = target.read_text()
    assert 'title="Cool API"' in content
    assert 'version="1.2.3"' in content
    assert 'summary="Does things"' in content
    assert "{{" not in content


def test_apply_metadata_tolerates_quote_and_spacing_variations(tmp_path, monkeypatch):
    target = write_template(
        tmp_path,
        "FastAPI(\n"
        "    title='{{project_name}}',\n"
        '    version = "{{  project_version  }}",\n'
        ")\n",
    )
    monkeypatch.chdir(tmp_path)

    main.apply_project_metadata({"name": "API", "version": "9.9", "description": "x"})

    content = target.read_text()
    # only the placeholder token is replaced; surrounding quotes are preserved
    assert "title='API'" in content
    assert 'version = "9.9"' in content
    assert "{{" not in content


def test_apply_metadata_replaces_placeholders_across_all_files(tmp_path, monkeypatch):
    services = tmp_path / "app" / "services"
    services.mkdir(parents=True)
    (services / "auth.py").write_text('subject = "Welcome to {{ project_name }}"\n')
    (tmp_path / "README.md").write_text("# {{ project_name }} v{{ project_version }}\n")
    monkeypatch.chdir(tmp_path)

    main.apply_project_metadata(
        {"name": "Ledger", "version": "2.0.0", "description": "d"}
    )

    assert (services / "auth.py").read_text() == 'subject = "Welcome to Ledger"\n'
    assert (tmp_path / "README.md").read_text() == "# Ledger v2.0.0\n"


def test_apply_metadata_skips_git_directory(tmp_path, monkeypatch):
    git_file = tmp_path / ".git" / "COMMIT_EDITMSG"
    git_file.parent.mkdir()
    git_file.write_text("{{ project_name }}\n")
    monkeypatch.chdir(tmp_path)

    main.apply_project_metadata({"name": "Ledger", "version": "1", "description": "d"})

    # files under .git must be left untouched
    assert git_file.read_text() == "{{ project_name }}\n"


def test_apply_metadata_skips_binary_files(tmp_path, monkeypatch):
    (tmp_path / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n\xff\xfe{{ project_name }}")
    (tmp_path / "app.py").write_text("name = '{{ project_name }}'\n")
    monkeypatch.chdir(tmp_path)

    # a binary file that fails to decode must not abort the whole pass
    main.apply_project_metadata({"name": "X", "version": "1", "description": "d"})

    assert "name = 'X'" in (tmp_path / "app.py").read_text()


def test_apply_metadata_does_not_serialize_description_as_a_list(tmp_path, monkeypatch):
    target = write_template(tmp_path, 'FastAPI(summary="{{ project_description }}")\n')
    monkeypatch.chdir(tmp_path)

    main.apply_project_metadata(
        {"name": "n", "version": "v", "description": "plain text"}
    )

    assert 'summary="plain text"' in target.read_text()


def test_apply_metadata_inserts_regex_special_characters_literally(
    tmp_path, monkeypatch
):
    # A description containing a regex backreference (\1) or metacharacters must
    # be written verbatim, not interpreted by re.sub.
    target = write_template(tmp_path, 'FastAPI(summary="{{ project_description }}")\n')
    monkeypatch.chdir(tmp_path)

    main.apply_project_metadata(
        {"name": "n", "version": "v", "description": r"money & \1 backref"}
    )

    assert r'summary="money & \1 backref"' in target.read_text()


def test_apply_metadata_is_noop_when_no_files_present(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # empty project tree

    # should not raise when there is nothing to process
    main.apply_project_metadata({"name": "n", "version": "v", "description": "d"})

    assert list(tmp_path.iterdir()) == []


# --- run_command -----------------------------------------------------------


def test_run_command_invokes_subprocess_with_check(monkeypatch):
    seen = {}

    def fake_run(cmd, **kwargs):
        seen["cmd"] = cmd
        seen["check"] = kwargs.get("check")

    monkeypatch.setattr(subprocess, "run", fake_run)

    main.run_command(["echo", "hi"])

    assert seen == {"cmd": ["echo", "hi"], "check": True}


def test_run_command_propagates_command_failure(monkeypatch):
    def failing_run(cmd, **kwargs):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", failing_run)

    with pytest.raises(subprocess.CalledProcessError):
        main.run_command(["false"])


# --- generate_project_scaffold ---------------------------------------------


def stub_scaffold(monkeypatch, tmp_path, run_impl):
    """Run generate_project_scaffold against tmp_path with git/clone stubbed out."""
    monkeypatch.chdir(tmp_path)

    def fake_clone(slug, *args, **kwargs):
        (tmp_path / slug).mkdir()

    monkeypatch.setattr(main, "clone_template_repository", fake_clone)
    monkeypatch.setattr(main, "run_command", run_impl)


def sample_detail(**overrides):
    detail = {
        "slug": "proj",
        "name": "Proj",
        "description": "desc",
        "version": "1.0.0",
        "authors": "Jane Dev",
        "open_source_license": "MIT",
        "repository_link": "https://example.com/repo.git",
    }
    detail.update(overrides)
    return detail


def test_generate_scaffold_exits_when_directory_exists(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "proj").mkdir()

    with pytest.raises(SystemExit) as exit_info:
        main.generate_project_scaffold(sample_detail())

    assert exit_info.value.code == 1
    assert "Directory already exists" in capsys.readouterr().out


def test_generate_scaffold_resets_history_before_committing(tmp_path, monkeypatch):
    calls = []
    stub_scaffold(monkeypatch, tmp_path, lambda cmd: calls.append(cmd))

    main.generate_project_scaffold(sample_detail())

    commit = ["git", "commit", "-m", "Save Metadata Changes"]
    assert ["rm", "-rf", ".git"] in calls
    assert ["git", "init"] in calls
    assert ["git", "add", "-A"] in calls
    assert commit in calls
    assert ["git", "remote", "add", "origin", "https://example.com/repo.git"] in calls
    # history is wiped and re-initialised before the first commit is created
    assert calls.index(["rm", "-rf", ".git"]) < calls.index(["git", "init"])
    assert calls.index(["git", "init"]) < calls.index(commit)
    # a LICENSE file is generated (and staged before the commit)
    assert (tmp_path / "proj" / "LICENSE").read_text().startswith("MIT License")


def test_generate_scaffold_skips_remote_when_link_missing(
    tmp_path, monkeypatch, capsys
):
    calls = []
    stub_scaffold(monkeypatch, tmp_path, lambda cmd: calls.append(cmd))

    main.generate_project_scaffold(sample_detail(repository_link=""))

    assert not any(cmd[:3] == ["git", "remote", "add"] for cmd in calls)
    assert "No repository link provided" in capsys.readouterr().out


def test_generate_scaffold_continues_when_commit_fails(tmp_path, monkeypatch, capsys):
    def run_with_failing_commit(cmd):
        if cmd[:2] == ["git", "commit"]:
            raise subprocess.CalledProcessError(1, cmd)

    stub_scaffold(monkeypatch, tmp_path, run_with_failing_commit)

    main.generate_project_scaffold(sample_detail())

    assert "Could not create initial commit" in capsys.readouterr().out


# --- main (orchestration) --------------------------------------------------


def test_main_collects_all_details_and_generates(monkeypatch):
    # empty input at every prompt -> defaults are used throughout
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr("sys.argv", ["fastapi-gen8"])

    generated = {}
    monkeypatch.setattr(
        main, "generate_project_scaffold", lambda detail: generated.update(detail)
    )

    main.main()

    assert set(generated) == set(main.DEFAULT_PROJECT_DETAIL)
    assert generated["slug"] == "awesome_fastapi_project"
    assert generated["open_source_license"] == "MIT"
