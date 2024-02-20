from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")


# Initiate like this when using organization account
client = OpenAI(
  organization=ORGANIZATION_ID,
  api_key=API_KEY
)

'''
Legacy models: 
    endpoint: https://api.openai.com/v1/completions
    model ids:
        gpt-3.5-turbo-instruct
        babbage-002
        davinci-002
Newer models
    endpoint: https://api.openai.com/v1/chat/completions
    model ids:
        gpt-4
        gpt-4-turbo-preview
        gpt-3.5-turbo
'''
'''Run this first if unsure the API is properly setted'''
# response = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     # {"role": "system", "content": "You are a helpful assistant."},
#     # {"role": "user", "content": "Hello!"}
#     {"role": "user", "content": "Say this is a test!"}
#   ],
#   stream=False
# )

response = client.chat.completions.create(
  # model="gpt-4-turbo-preview",
#   model="gpt-4",
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "How many moons saturn have? What are their names and sizes? Are any of them livable?"}
  ],
  stream=False
#   max_tokens=256,
#   max_tokens=1024,
    # dont use temperature AND top_p, only one or other
#   temperature=0.7 #between 0 and 2, lower = deterministic
#   top_p=1, # alternative of temperature, between 0 and 1
)


# Printing the response in terminal
print(f'Raw: {response}')
openai_responses = [ x.message.content for x in response.choices]
print('#\n\nResponse:\n\n') # empty line for visual separation in terminal
[ print(f'{x}\n') for x in openai_responses ]






