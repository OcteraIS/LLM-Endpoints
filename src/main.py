from dotenv import load_dotenv
import os
from api.openai_api import OpenAI_OrganizationAPI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION_ID = os.getenv("OPENAI_ORGANIZATION_ID")

openai_api = OpenAI_OrganizationAPI(
    OPENAI_API_KEY,
    OPENAI_ORGANIZATION_ID,
    debug_print=True
)

openai_api.run_verification()

# openai_api.complex_prompt_usage_example()

