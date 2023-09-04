from dotenv import load_dotenv
import os

load_dotenv('.env')
open_api_key = os.getenv('OPENAI_API_KEY')
pexels_api_key = os.getenv('PEXELS_API_KEY')
eleven_labs_api_key = os.getenv('ELEVEN_LABS_API_KEY')
