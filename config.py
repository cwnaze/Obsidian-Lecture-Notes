import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the root
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/oln_db')
    API_KEY: str = os.getenv('API_KEY', '')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT: int = int(os.getenv('PORT_BACKEND', '8000'))

settings = Settings()
