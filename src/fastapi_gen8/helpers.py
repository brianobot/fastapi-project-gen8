import subprocess


def slugify(text: str) -> str:
    return text.replace(" ", "_").replace("-", "_").lower()

def success_print(value: str):
    print("\033[92m{}\033[00m".format(value))

def warning_print(value: str):
    print("\033[33m{}\033[00m".format(value))

def error_print(value: str):
    print("\033[31m{}\033[00m".format(value))


def clone_repository(repository_url: str, folder_name: str):
    try:
        clone_template_repo = subprocess.Popen(["git", "clone", repository_url, folder_name])
        clone_template_repo.wait()
    except Exception as err:
        error_print(f"Failed to Download Template: Reason: {err}")
        exit(1)
    
    
