import time
import json
import subprocess
from typing import cast
from pathlib import Path


def intro_text() -> None:
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
                                                                 
     ██████╗ ███████╗███╗   ██╗███████╗ █████╗     
    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗    
    ██║  ███╗█████╗  ██╔██╗ ██║█████╗   █████╔╝   
    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗  
    ╚██████╔╝███████╗██║ ╚████║███████╗ █████╔╝  
        ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═══╝ ╚════╝    
    ______________________________________________________________
    """
    print(intro_message)
    description = """
    Generate a fully structured FastAPI projects instantly.  
    Boilerplate code, ready-to-run endpoints, and project scaffolding  
    all in one simple command. Kickstart your backend in seconds!
    
    Provide Project Details to each prompt and press Enter complete project setup
    Values placed within square brackets ([My Awesome FastAPI Project]) are defaults values for the project details
    If you do not provide a value, those values are used instead
    
    FUN 🚀
    How Fast Can you Complete your FastAPI project setup?
    Blaze through the steps to make the global leaderboard for projects generated with FastAPI Project Gen8.
    In Order to qualify for this leaderboard, you have to make sure to input every project detail and not use defaults
    even though the defaults match your project attribute.
    
    Current Best Record: {get_current_best_record()[0]} seconds - Title: [{get_current_best_record()[1]}] 
    """
    print(description)
    
    
def get_project_detail(
    attr: str, 
    default: str | int | tuple[str, ...], 
    project_detail: dict[str, str | int | tuple]
) -> str | int | tuple[str, ...]:
    # Process the display for collecting the detail
    if "_" in attr:
        attr = attr.lower()
    if attr == "slug_name":
        default = slugify(str(project_detail['name']))
    
    if attr not in {"open_source_license", "username_type"}:
        detail = input(f"Enter Project {attr} ['{default}']: ")
    else:
        count = 0
        detail = ""
        is_not_valid = True
        default_index = int(cast(tuple, project_detail[attr])[0]) - 1
        default = cast(tuple, project_detail[attr])[1][default_index][1]
        
        while is_not_valid:
            options = cast(tuple[str, list[tuple[int, str]]], project_detail[attr])[1]
            print(f"Select {attr}:")
            for index, option in options:
                print(f"\t{index} - {option}")
            
            prompt_msg = f"Choose from {', '.join(str(i) for i in range(index))}: [{cast(tuple, project_detail[attr])[0]}]: "
            detail_index = input(prompt_msg)

            if not detail_index or detail_index.isspace():
                detail = default
                is_not_valid = False
            elif not detail_index.isdigit():
                warning_print(f"Invalid Value {detail_index} for {attr}... Please Try Again!")
            elif int(detail_index) not in range(index + 1):
                warning_print(f"Invalid Value {detail_index} for {attr}... Please Try Again!")
            else:
                detail = detail = cast(tuple, project_detail[attr])[1][int(detail_index) - 1][1]
                is_not_valid = False
                
            count += 1
            if count > 3:
                break
        
        if count >= 3:
            error_print(f"Failed Due to repeated (X3) Invalid Value for {attr}")
            exit(1)
    
    # Process the value provided by the user
    if attr == "slug_name":
        detail = slugify(cast(str, detail))
    if attr == "authors":
        detail = tuple(cast(str, detail).split(","))
    return detail if detail else default


def generate_project(project_detail: dict[str, str]):
    # Clone The Default Project Template into Folder with Project Slug Name
    # check if the project already exist
    result = None
    if Path(f"{project_detail['slug_name']}").exists():
        warning_print("Directory Already Exist")
    else:
        result = subprocess.Popen(["git", "clone", "https://github.com/brianobot/fastAPI_project_structure", f"{project_detail['slug_name']}"])
    print(f"✅✅✅ Result = {result}")


def slugify(text: str) -> str:
    return text.replace(" ", "_").replace("-", "_").lower()

def success_print(value: str):
    print("\033[92m{}\033[00m".format(value))

def warning_print(value: str):
    print("\033[33m{}\033[00m".format(value))

def error_print(value: str):
    print("\033[31m{}\033[00m".format(value))


def main():
    intro_text()
    project_details: dict[str, str | int | tuple] = {
        "name": "My Awesome FastAPI Project",
        "slug_name": "my_awesome_fastapi_project",
        "description": "FastAPI Backend Project",
        "authors": ("John Doe", "Jane Doe"),
        "version": "0.1.0",
        "email": "brianobot9@gmail.com",
        "open_source_license": ("1", [
            (1, "MIT"), 
            (2, "BSD"), 
            (3, "GPLv3"), 
            (4, "Apache Software License 2.0"), 
            (5, "Not open source"),
        ]),
        "username_type": ("1", [
            (1, "email"),
            (2, "username"),
            (3, "email + username"),
        ]),        
    }
    
    start_time = time.time()
    for attr, default_value in project_details.items():
        detail = get_project_detail(attr.title(), default_value, project_details)
        project_details[attr] = detail
        success_print(f"Project {attr.title()} = {detail}")
        
    
    elapsed_time = time.time() - start_time
    print("----------------------------------------------")
    success_print(f"Elasped Time: {elapsed_time:.4f} secs 🎉🎉")
    print("----------------------------------------------")
    json.dump(project_details, open("data.json", "w"))

    # Generate Projects with the Details Provided by the User
    generate_project(cast(dict[str, str], project_details))


if __name__ == "__main__":
    main()