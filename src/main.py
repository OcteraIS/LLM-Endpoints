from dotenv import load_dotenv
import os
from api.openai_api import OpenAI_OrganizationAPI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION_ID = os.getenv("OPENAI_ORGANIZATION_ID")

openai_api = OpenAI_OrganizationAPI(
    OPENAI_API_KEY,
    OPENAI_ORGANIZATION_ID
)
openai_api.test_call()

'''

api = OpenAI_OrganizationAPI()

api.long_term_memory(conversation_id=ID, prompt)
api.new_long_term_memory(prompt) -> ID
api.single_prompt()

'''