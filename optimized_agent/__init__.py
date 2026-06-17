from dotenv import load_dotenv
from pathlib import Path

# Load local .env in the optimized_agent package so secrets are available
load_dotenv(Path(__file__).parent / ".env")

from . import agent
