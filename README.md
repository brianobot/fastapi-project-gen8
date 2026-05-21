# FastAPI Gen8

FastAPI Project Gen8 is a lightweight command-line tool designed to generate clean, structured, production-ready FastAPI project scaffolds at warp speed.

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

Generate a Functional FastAPI Projects in Seconds 🚀

## Overview

FastAPI Gen8 is a lightweight command-line tool designed to generate clean, structured, production-ready FastAPI project scaffolds at warp speed.
Whether you're spinning up a new microservice or testing a prototype idea, Gen8 gives you a fresh, organized foundation with sensible defaults — so you can focus on building, not boring setup rituals.


### Prerequisites

Before igniting the generator, make sure you've completed the following:

- Create a remote Git repository for your new project.
- Optionally Setup a Database (E.g, Postgres, MySQL) for your FastAPI App
- Setup a Redis Server running on your machine


Gen8 will automatically initialize Git and link your project to the remote origin you provide.

## Features

- Instant FastAPI project scaffold.
- Automatic Git initialization + remote origin setup.
- Clean directory structure and preconfigured templates.
- Opinionated defaults with sensible fallbacks.
- Fast, simple, and repeatable.

Installation
```bash
pip install fastapi-gen8
```

Usage
```bash
fastapi-gen8
```
![Introduction Screenshot](images/intro_demo.png)


You’ll be prompted for project details such as name, slug, description, and Git remote URL.
and also following through, a FastAPI project would be generated for you with those details.
You can use the README on the generated project to verify and complete the project setup like updating .env file
and running your first unit test on the project.

### Note:
The generated project comes with a comprehensive Unit tests for the code it contains

### Example
```bash
fastapi-gen8
```

#### Project Structure
A typical generated project looks like:

```
<project_slug_name>/
├── app/
│   ├── main.py
│   ├── routers/
│   ├── models/
│   ├── services/
│   ├── __init__.py
│   ├── main.py
│   ├── api_router.py
│   ├── dependencies.py
│   ├── logger.py
│   ├── middlewares.py
│   ├── mailer.py
│   ├── redis_manager.py
│   └── utils
├── requirements.txt
├── alembic/
├── alembic.ini
├── .gitignore
├── README.md
└── ...
```

## Why FastAPI Gen8?

- Because the world moves too fast for boilerplate.
- Because creativity should start at the endpoint, not the folder tree.
- Because momentum matters — and FastAPI Gen8 gives you that first push.

## License
- [MIT License](LICENSE)
