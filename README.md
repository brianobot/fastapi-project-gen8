# FastAPI Gen8

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

Generate FastAPI Projects in Seconds

## Overview

FastAPI Project Gen8 is a lightweight command-line tool designed to generate clean, structured, production-ready FastAPI project scaffolds at warp speed.
Whether you're spinning up a new microservice or testing a prototype idea, Gen8 gives you a fresh, organized foundation with sensible defaults — so you can focus on building, not boring setup rituals.

### Prerequisites

Before igniting the generator, make sure you've completed the following:

- Create a remote Git repository for your new project.
- Operational Postgres or Any Other database running on your machine
- Operation Redis Server running on your machine


Gen8 will automatically initialize Git and link your project to the remote origin you provide.
(Think of it as handing the newborn project its first passport.)

## Features

- Instant FastAPI project scaffold
- Automatic Git initialization + remote origin setup
- Clean directory structure and preconfigured templates
- Opinionated defaults without being bossy
- Fast, simple, and repeatable — like a well-trained cosmic forge

Installation
```bash
pip install fastapi-project-gen8
```

(or whatever installation method your tool uses — adjust as needed.)

Usage
```bash
fastapi-gen8
```

You’ll be prompted for project details such as name, slug, description, and Git remote URL.
Then—whoosh!—a fully structured FastAPI project appears in your universe.

### Example
fastapi-gen8 --name "my-awesome-api" --remote "git@github.com:me/my-awesome-api.git"

#### Project Structure
A typical generated project looks like:

my-awesome-api/
├── app/
│   ├── main.py
│   ├── routers/
│   └── core/
├── requirements.txt
├── .gitignore
├── README.md
└── ...

## Why FastAPI Gen8?

- Because the world moves too fast for boilerplate.
- Because creativity should start at the endpoint, not the folder tree.
- Because momentum matters — and FastAPI Gen8 gives you that first push.

## License
- MIT License
