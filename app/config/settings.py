"""
This file contains configuration settings for the application,
such as environment variables and constants.
"""
import os
from pathlib import Path

from dotenv import main
from pydantic import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

main.load_dotenv()

def load_env_var_strict(name: str) -> str:
    """Loads an environment variable and raises an error if not set."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value
## Loading Environment Variables
JWT_AUTH_SECRET_KEY = load_env_var_strict('JWT_AUTH_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50

## Configuration Settings
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
BASE_DIR = Path(__file__).resolve().parent.parent

if DB_TYPE == "postgres":
    # PostgreSQL Database Configuration
    POSTGRES_USER = load_env_var_strict('POSTGRES_USER')
    POSTGRES_DATABASE = load_env_var_strict('POSTGRES_DATABASE')
    POSTGRES_PASSWORD = load_env_var_strict('POSTGRES_PASSWORD')
    POSTGRES_HOST = load_env_var_strict('POSTGRES_HOST')
    POSTGRES_PORT = load_env_var_strict('POSTGRES_PORT')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
else:
    # SQLite Database Configuration
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/db.sqlite3"

## Loading Environments Variable
TAVILY_API_KEY = load_env_var_strict('TAVILY_API_KEY')



LANGFUSE_SECRET_KEY = load_env_var_strict('LANGFUSE_SECRET_KEY')
LANGFUSE_PUBLIC_KEY = load_env_var_strict('LANGFUSE_PUBLIC_KEY')
LANGFUSE_HOST = os.getenv('LANGFUSE_HOST', 'http://localhost:3000')

# Langfuse Configuration
LANGFUSE_CONFIG = {
    'secret_key': LANGFUSE_SECRET_KEY,
    'public_key': LANGFUSE_PUBLIC_KEY,
    'host': LANGFUSE_HOST
}
from langfuse.callback import CallbackHandler
from langfuse.decorators import observe
langfuse_handler = CallbackHandler(**LANGFUSE_CONFIG)


# ORM Engine Configuration
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if DB_TYPE == "sqlite" else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base ORM Model
Base = declarative_base()
Base.metadata.create_all(bind=engine)

# DB Utilities
def get_session():
    ''' Return Database ORM Session Object'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


AGENT_CONFIG_RUNABLE = {"thread_id": 42}
DEFAULT_INDEX_PATH = load_env_var_strict("DEFAULT_INDEX_PATH")
DEFAULT_INDEX_PATH = BASE_DIR/DEFAULT_INDEX_PATH
RELEVENCY_CHECK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RELEVENCY_SCORE_THRESH=0.7
### LLM Model Configuration
LLM_PROVIDER=load_env_var_strict('LLM_PROVIDER')
if LLM_PROVIDER=='groq':
    GROQ_API_KEY = load_env_var_strict('GROQ_INFERENCE_API_KEY')
    GROQ_MODEL_NAME  = "mixtral-8x7b-32768"
    from langchain_groq import ChatGroq
    default_llm_model = ChatGroq(model=GROQ_MODEL_NAME,
            temperature=0.3, api_key=SecretStr(GROQ_API_KEY))

elif LLM_PROVIDER=='azure_openai':
    OPENAI_MODEL_NAME = 'gpt-4o'
    AZURE_OPENAI_ENDPOINT = load_env_var_strict('AZURE_OPENAI_ENDPOINT')
    from langchain_openai import AzureChatOpenAI
    default_llm_model = AzureChatOpenAI(model_name="gpt-4o" )

EMBEDDING_MODEL_PROVIDER = load_env_var_strict('EMBEDDING_MODEL_PROVIDER')
# Embedding Model Configuration
if EMBEDDING_MODEL_PROVIDER=="azure_openai":
    model_name=load_env_var_strict('OPENAI_EMBEDDING_MODEL_NAME')
    from langchain_openai import AzureOpenAIEmbeddings
    embed_model = AzureOpenAIEmbeddings(model=model_name)
    EMBEDDING_MODEL_VECTOR_LENGTH=int(load_env_var_strict("EMBEDDING_DIMENTION"))
    # embed_model.embed_documents = observe(as_type="generation")(embed_model.embed_documents)
    # embed_model.embed_query = observe(as_type="generation")(embed_model.embed_query)
else:
    from langchain_huggingface import HuggingFaceEmbeddings

    embed_model = HuggingFaceEmbeddings(model_name="Alibaba-NLP/gte-base-en-v1.5",
                                    model_kwargs = {'trust_remote_code': True})
    EMBEDDING_MODEL_VECTOR_LENGTH = len(embed_model.embed_query("Hello World"))

    # embed_model.embed_documents = observe(as_type="generation")(embed_model.embed_documents)
    # embed_model.embed_query = observe(as_type="generation")(embed_model.embed_query)
print(dir(embed_model)) 