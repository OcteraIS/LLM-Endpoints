from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")


'''

api = OpenAI_OrganizationAPI()

api.long_term_memory(conversation_id=ID, prompt)
api.new_long_term_memory(prompt) -> ID
api.single_prompt()

'''