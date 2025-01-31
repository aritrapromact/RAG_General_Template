"""
This file contains configuration settings for the application,
such as environment variables and constants.
"""

import os
from pathlib import Path 
from dotenv import main
main.load_dotenv()



def load_env_var_strict(name: str) -> str:
    """This function loads an environment variable with the specified name. If the environment variable is not set, it raises
    a ValueError."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value
## Loading Environment Variables
JWT_AUTH_SECRET_KEY = load_env_var_strict('JWT_AUTH_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50


BASE_DIR = Path(__file__).resolve().parent.parent

# # PostgreSQL Database Configuration
POSTGRES_USER = load_env_var_strict('POSTGRES_USER')
POSTGRES_DATABASE = load_env_var_strict('POSTGRES_DATABASE')
POSTGRES_PASSWORD = load_env_var_strict('POSTGRES_PASSWORD')
POSTGRES_HOST = load_env_var_strict('POSTGRES_HOST')
POSTGRES_PORT = load_env_var_strict('POSTGRES_PORT')


## ORM Engine Configuration
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

GROQ_API_KEY = load_env_var_strict('GROQ_INFERENCE_API_KEY')
GROQ_MODEL_NAME  = "mixtral-8x7b-32768"