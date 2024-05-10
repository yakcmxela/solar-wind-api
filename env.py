import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
DATABASE_URL=os.getenv("DATABASE_URL")
AMBIENT_API_KEY=os.getenv("AMBIENT_API_KEY")
AMBIENT_APPLICATION_KEY=os.getenv("AMBIENT_APP_KEY")