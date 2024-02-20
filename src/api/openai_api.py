from openai import OpenAI
from openai import ChatCompletion

class OpenAI_OrganizationAPI:

  __test_message = {"role": "user", "content": "Say this is a test!"}
  __default_messages = {"role": "system", "content": "You are a helpful assistant."}

  def __init__(self, API_KEY, ORGANIZATION_ID):
    self.API_KEY = API_KEY
    self.ORGANIZATION_ID = ORGANIZATION_ID
    self.client = OpenAI(
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
  def __api(self, model, messages, stream=False) -> ChatCompletion:

    # Legacy model identifiers
    new_models = ['gpt-4', 'gpt-4-turbo-preview', 'gpt-3.5-turbo', ]

    # If model passed is not one of the expected ones, print error and end
    if model not in new_models:
      print(f'Unespected OpenAI model name: {model}')
      print(f'Available models: {new_models}')
    else: # If everything's ok, call the API
      server_response = self.client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
      )
      return server_response

  def __legacy_api(self, model, message) -> ChatCompletion:
    
    # Legacy model identifiers
    legacy = ['gpt-3.5-turbo-instruct', 'babbage-002', 'davinci-002']

    # If model passed is not one of the expected ones, print error and end
    if model not in legacy:
      print(f'Unespected legacy OpenAI model name: {model}')
      print(f'Available models: {legacy}')
    else: # If everything's ok, call the API
      server_response = self.client.completions.create(
        model=model,
        prompt=message
      )
      return server_response

  
  def legacy_test_call(self, print_result=True) -> bool:

    # Make sure the program wont halt by a bad api call/unwrap
    try:

      # Call OpenAI endpoint. Any model works, hence calling the cheapest one
      response = self.__legacy_api(
        model="gpt-3.5-turbo-instruct",
        messages=[
          {"role": "user", "content": "Say this is a test!"}
        ],
      )

      # response = response.choices[0].message.content
      response = response.choices[0].text
      status = '✅' if response == 'This is a test!' else '⛔'

      if print_result:
        print(f'{status} Server response is \'{response}\'')
      return True
    except Exception as e:
      print(e)

  # TODO: finish __legacy_api, __api, legacy_test_call, and test_call

  def single_prompt():
    pass

  def long_term_memory():
    pass

  def new_long_term_memory():
    pass





# response = client.chat.completions.create(
#   # model="gpt-4-turbo-preview",
# #   model="gpt-4",
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "How many moons saturn have? What are their names and sizes? Are any of them livable?"}
#   ],
#   stream=False
# #   max_tokens=256,
# #   max_tokens=1024,
#     # dont use temperature AND top_p, only one or other
# #   temperature=0.7 #between 0 and 2, lower = deterministic
# #   top_p=1, # alternative of temperature, between 0 and 1
# )


# # Printing the response in terminal
# print(f'Raw: {response}')
# openai_responses = [ x.message.content for x in response.choices]
# print('#\n\nResponse:\n\n') # empty line for visual separation in terminal
# [ print(f'{x}\n') for x in openai_responses ]






