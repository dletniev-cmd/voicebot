import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
GROQ_API_KEY: str = os.environ["GROQ_API_KEY"]
