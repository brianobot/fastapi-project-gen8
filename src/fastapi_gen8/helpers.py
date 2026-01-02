import subprocess


def display_intro_text() -> None:
    """
    Displays the Introduction Text of the Library as a Nice and Friendly UI
    Alongside a short instructions on how to use the library for new users.
    """
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
                                                                 
     ██████╗ ███████╗███╗   ██╗ █████╗     
    ██╔════╝ ██╔════╝████╗  ██║██╔══██╗    
    ██║  ███╗█████╗  ██╔██╗ ██║ █████╔╝   
    ██║   ██║██╔══╝  ██║╚██╗██║██╔══██╗  
    ╚██████╔╝███████╗██║ ╚████║ █████╔╝  
        ╚═════╝ ╚══════╝╚═╝  ╚╝ ╚════╝    
    ______________________________________________________________
    """
    print(intro_message)
    description = """
    Generate a fully structured FastAPI projects instantly.  
    Boilerplate code, ready-to-run endpoints, and project scaffolding  
    all in one simple command. Kickstart your backend in seconds!
    
    Provide Project Details to each prompt and press 'Enter' to complete project setup
    
    NOTES: Values placed within square brackets ([My Awesome FastAPI Project]) are defaults values for the project details
    If you do not provide a value for any particular, those values are used instead.
    
    Have a Blast 🚀 - Brian
    _____________________________________________________________________________________________________
    """
    # FUN 🚀
    
    # How Fast Can you Complete your FastAPI project setup?
    # Blaze through the steps to make the global leaderboard for projects generated with FastAPI Project Gen8.
    # In Order to qualify for this leaderboard, you have to make sure to input every project detail and not use defaults
    # even though the defaults match your project attribute.
    # Current Best Record: {get_current_best_record()[0]} seconds - Title: [{get_current_best_record()[1]}] 
    print(description)


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
    
    
