from dotenv import load_dotenv
import os
from api.gemini_api import GeminiAPI
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

# This line verifies if everything is ok. You can delete it after testing it
openai_api.run_verification()

# ========================================================================
#                       MARK: Write your code here
    # To know which functions to use, look at documentation (../README.md)
    # Or alternatively, you can read the code in ./api/openai_api.py 
        # (it follows project documentation patterns)
# ========================================================================

