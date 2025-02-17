# RAG_General_Template

A FastAPI project for creating applications using the Retrieval-Augmented Generation (RAG) approach.


## Projecr Startup Information
* Run Project via uv :
  - As this Project is uv Dependent it will be very easy to run projects with uv. This required installed uv in your global environment.
  - Install UV via PIP :`pip install uv` 
  - Install uv Directly : `powershell -c "irm https://astral.sh/uv/install.ps1 | more"`
  - Run Projects :`uv run uvicorn main:app --reload`

* Run Project Without uv :
  - Create Python Virtual env using venv : `python -m venv env`
  - Activate Virtual env : `.\env\Scripts\activate`
  - Install Dependencies : `pip install -r requirements.txt`
  - Run Projects :`uvicorn main:app --reload`


## Additional Setup Information 

* Database : 
  - Setup Postgresql Database in your local or Server and add Cred into .env file or Environment Variable 
  - Setup the DB_TYPE variable with database name `postgres`
* Monitoring Tool : 
  - Use **Langfuse** as monitoring Tools add Langfuse config on env 
  - Setup langfuse on Docker  or use langfuse cloud url : [text](https://cloud.langfuse.com/)
## Folder Structure

```plaintext
RAG_General_Template/
├── app/                            # Main application logic.
│   ├── main.py                     # Entry point of the application.
│   ├── __init__.py                 # Package marker.
│   ├── config/                     # Application configurations (settings, logging).
│   │   ├── settings.py             # Configuration settings.
│   │   ├── logging_config.py       # Logging configuration.
│   ├── core/                       # Core functionalities (authentication, constants).
│   │   ├── auth.py                 # Authentication logic.
│   │   ├── constants.py            # Core constants.
│   ├── db/                         # Database setup and ORM models.
│   │   ├── models/                 # ORM models for database tables.
│   │   │   ├── chat_history.py     # Chat history model.
│   │   │   ├── user.py             # User model.
│   ├── routes/                     # API endpoint route definitions.
│   │   ├── conversation.py         # Conversation-related routes.
│   │   ├── users.py                # User-related routes.
│   ├── schemas/                    # Pydantic schemas for data validation.
│   │   ├── auth.py                 # Authentication schemas.
│   │   ├── chat.py                 # Chat-related schemas.
│   │   ├── user.py                 # User schemas.
│   ├── services/                   # Service layer for business logic.
│   │   ├── RAG/                    # RAG component services.
│   │   │   ├── document_parser.py  # Document parsing logic.
│   │   │   ├── llm_search.py       # Language model search logic.
│   │   │   ├── prompts.py          # Prompt management.
│   │   │   ├── vectorstore.py      # Vector storage management.
│   ├── tests/                      # Unit and integration tests.
│   │   ├── test_items.py           # Tests for item routes.
│   │   ├── test_users.py           # Tests for user routes.
├── scripts/                        # Utility scripts.
├── pyproject.toml                  # PyProject TOML file.
├── .gitignore                      # Git ignore file.
├── requirements.txt                # Project dependencies.
└── README.md                       # Project README file.
```
## Project Overview

This project provides a template for creating applications using the Retrieval-Augmented Generation (RAG) approach. It includes various components for handling AI-driven interactions, data storage, and API endpoints.

## Detailed Module Description

### app/main.py
The main entry point of the application. It initializes the FastAPI app and configures routes and middleware.

### app/config/
Contains configuration files for settings and logging.

- **settings.py**: 
  This file contains configuration settings for the application, such as environment variables and constants. Key features include:
  - **Environment Variables**: Utilizes the `dotenv` package to load environment variables, ensuring that critical settings like `JWT_AUTH_SECRET_KEY`, `TAVILY_API_KEY`, and database credentials are securely managed.
  - **Database Configuration**: Supports both PostgreSQL and SQLite, dynamically configuring the SQLAlchemy database URL based on the `DB_TYPE` environment variable.
  - **Security Settings**: Configures JWT authentication settings, including the secret key and algorithm.
  - **API Keys and Hosts**: Manages API keys and host configurations for external services like `LANGFUSE`.
- **logging_config.py**: Configures logging for the application.

### app/core/
This module contains core functionalities such as authentication and constants. Key features include:

- **auth.py**: 
  - Defines authentication-related API endpoints and helper functions.
  - Implements password hashing and verification using `passlib`.
  - Provides JWT-based authentication mechanisms, including token creation and user authentication.
  - Includes functions to check if an email or username is already taken in the database.
- **constants.py**: 
  - Contains constant values used across the core module, ensuring consistency and reducing hard-coded values.
- **dependencies.py**: Manages dependency injection.
- **events.py**: Handles application events.

### app/db/
This module is responsible for setting up the database and defining the ORM models using SQLAlchemy. It includes the following components:

- **Base Class**: All ORM models inherit from the `Base` class, which is configured in the settings module. This serves as the declarative base for SQLAlchemy models.

- **Models**: The `models` directory contains the ORM models that define the database schema.

  - **chat_history.py**: 
    - Defines the `Conversation` model, which represents chat history.
    - Contains fields such as `conversation_id`, `user_id`, and `history`.
    - Establishes a relationship with the `User` model, allowing for easy retrieval of user-related conversation history.

  - **user.py**: 
    - Defines the `User` model, which represents user data.
    - Contains fields such as `user_id`, `username`, `email`, and `_password_hash`.
    - Establishes a relationship with the `Conversation` model, enabling user-specific conversation tracking.

These models are crucial for managing user data and chat history within the application, providing a structured way to interact with the database.

### app/routes/
This module defines the API endpoint routes for the application, handling various user and conversation-related functionalities. It includes:

- **conversation.py**:
  - Manages conversation-related routes, allowing users to interact with their chat history.
  - **Endpoints**:
    - `GET /conversations`: Retrieves a list of conversations for the current user.
    - `GET /conversations/{id}`: Retrieves a specific conversation by ID.
    - `POST /conversations`: Creates a new conversation and processes user queries.

- **users.py**:
  - Handles user-related routes, including user creation and authentication.
  - **Endpoints**:
    - `POST /users`: Creates a new user account, ensuring unique email and username.
    - `POST /login`: Authenticates a user and returns an access token.
    - `GET /users/me`: Retrieves the current user's information.
    - `POST /upload`: Allows users to upload files, which are processed and stored.

These routes are essential for managing user interactions and data flow within the application, providing a structured way to handle API requests.

### app/schemas/
Pydantic schemas for data validation.

- **auth.py**: Authentication schemas.
- **chat.py**: Chat-related schemas.
- **user.py**: User data schemas.

### app/services/
Service layer for business logic.

- **RAG/document_parser.py**: Parses documents for RAG processing.
- **RAG/llm_search.py**: Manages language model search operations.
- **RAG/prompts.py**: Handles prompt management for interactions.
- **RAG/vectorstore.py**: Manages vector storage for embeddings.

#### app/services/RAG/
This module is the heart of the Retrieval-Augmented Generation (RAG) system, providing essential services for document processing, language model interactions, and vector storage. It includes:

- **document_parser.py**:
  - Provides functionality to parse PDF documents and extract text from each page.
  - **Functions**:
    - `parse_documents`: Parses PDF content and extracts text, returning a list of Document objects with metadata.
    - `context_parser_input`: Converts Document objects into context strings with XML-like tags.
    - `context_parser_output`: Extracts content and metadata from context strings.

- **llm_search.py**:
  - Manages interactions with language models to process queries and retrieve relevant document chunks.
  - **Functions**:
    - `get_relevent_chunks`: Filters retrieved document chunks based on relevance to the language model response.
    - `get_llm_response`: Retrieves relevant document chunks and invokes the language model to generate a response.

- **prompts.py**:
  - Contains prompt templates for guiding language model interactions.
  - **Features**:
    - `default_template_prompt`: A template for generating responses based on provided context and metadata.

- **vectorstore.py**:
  - Handles vector storage operations using FAISS for efficient similarity searches.
  - **Functions**:
    - `save_on_vector_store`: Saves documents to a FAISS vector store for later retrieval.
    - `similarity_search`: Performs similarity searches to find documents related to a query.
    - `validate_index_path`: Ensures the validity of the index path used for vector storage.

This module is crucial for enabling the RAG capabilities of the application, allowing it to efficiently process documents, interact with language models, and store/retrieve data using vector embeddings.


## Best Practice Tools

This section outlines the key tools used in our project for code formatting, linting, and type checking. Each tool is configured to maintain code quality and consistency across the project.

### Black: Python Code Formatter

Black is an opinionated code formatter that ensures consistent code style across your project. It's designed to be uncompromising, requiring minimal configuration.

- **GitHub**: [Black on GitHub](https://github.com/psf/black)
- **Documentation**: [Black Documentation](https://black.readthedocs.io/en/stable/)

#### Configuration in `pyproject.toml`

```toml
[tool.black]
line-length = 88
skip-string-normalization = true
exclude = '''/(
  \.git
  | \.mypy_cache
  | \.venv
  | \.venv2
  | \.venv3
  | build
  | dist
  | alembic
)/'''
```

**Explanation**:

- `line-length = 88`: Sets the maximum line length to 88 characters, which is Black's default.
- `skip-string-normalization = true`: Prevents Black from converting all string quotes to double quotes.
- `exclude`: Specifies directories and files that Black should not format. This includes version control, cache directories, virtual environments, and build artifacts.

### Ruff: Fast Python Linter

Ruff is a high-performance Python linter written in Rust. It can replace multiple traditional Python linters and fixers, offering significant speed improvements.

- **GitHub**: [Ruff on GitHub](https://github.com/charliermarsh/ruff)
- **Documentation**: [Ruff Documentation](https://beta.ruff.rs/docs/)

#### Configuration in `pyproject.toml`

```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "B", "W", "I", "C", "N"]
ignore = ["E501"]
exclude = [
  ".git",
  ".mypy_cache",
  ".venv",
  ".venv2",
  ".venv3",
  "build",
  "dist",
  "alembic/**/*",
  "*/__init__.py"
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]

[tool.ruff.isort]
known-third-party = ["fastapi", "pydantic", "sqlalchemy"]
```

**Explanation**:

- `line-length = 88`: Matches Black's default line length for consistency.
- `select`: Enables specific rule sets:
  - `E`: pycodestyle errors
  - `F`: Pyflakes
  - `B`: flake8-bugbear
  - `W`: pycodestyle warnings
  - `I`: isort
  - `C`: mccabe complexity
  - `N`: pep8-naming
- `ignore = ["E501"]`: Disables the line length check (E501) as it's handled by Black.
- `exclude`: Lists directories and files to be ignored by Ruff.
- `per-file-ignores`: Specifies rules to ignore for specific files. Here, unused imports (F401) are allowed in `__init__.py` files.
- `isort`: Configures import sorting, specifying known third-party libraries.

### mypy: Static Type Checker

mypy is an optional static type checker for Python that helps catch type-related errors before runtime.

- **GitHub**: [mypy on GitHub](https://github.com/python/mypy)
- **Documentation**: [mypy Documentation](https://mypy.readthedocs.io/en/stable/)

#### Configuration in `pyproject.toml`

```toml
[tool.mypy]
strict = true
disallow_untyped_defs = false
ignore_missing_imports = true
warn_unused_ignores = true
ignore_errors = false
exclude = '.*/__init__.py'

[[tool.mypy.overrides]]
module = ["fastapi", "pydantic", "sqlalchemy"]
ignore_missing_imports = true
```

**Explanation**:

- `strict = true`: Enables strict type checking for maximum type safety.
- `disallow_untyped_defs = false`: Allows functions without type annotations.
- `ignore_missing_imports = true`: Ignores errors from missing type stubs for third-party libraries.
- `warn_unused_ignores = true`: Warns about unnecessary ignore comments.
- `ignore_errors = false`: Ensures mypy reports all type errors.
- `exclude = '.*/__init__.py'`: Excludes `__init__.py` files from type checking.
- `overrides`: Specifies settings for specific modules, here ignoring missing imports for FastAPI, Pydantic, and SQLAlchemy.

These configurations ensure consistent code style, catch potential errors early, and maintain a high standard of code quality across the project.

