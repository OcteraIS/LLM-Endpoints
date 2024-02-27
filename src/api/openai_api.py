from typing import Iterable
from openai import OpenAI, ChatCompletion
from openai.types.chat import ChatCompletionMessageParam

class OpenAI_OrganizationAPI:

  # Newest model identifiers
  # Endpoint: endpoint: https://api.openai.com/v1/completions
  __new_models = [ "gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-4-1106-preview", "gpt-4-vision-preview", "gpt-4", "gpt-4-0314", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0125", "gpt-3.5-turbo-16k-0613"]
  
  # Legacy model identifiers
  # endpoint: https://api.openai.com/v1/chat/completions
  __legacy_models = ['gpt-3.5-turbo-instruct', 'babbage-002', 'davinci-002']
  

  def __init__(self, API_KEY, ORGANIZATION_ID, debug_print = True):
    self.API_KEY = API_KEY
    self.ORGANIZATION_ID = ORGANIZATION_ID
    self.client = OpenAI(
      organization=ORGANIZATION_ID,
      api_key=API_KEY
    )
    self.DEBUG_PRINT = debug_print
  
  def print_from_stream(stream):
    for chunk in stream:
      if chunk.choices[0].delta.content is not None:
          print(chunk.choices[0].delta.content, end="")

  # Calls OpenAI API with memory using any of the 
  # newest models and returns the LLM anwer
    # If stream == true, function will return stream pointer
    # Otherwise, it will return json object
    # Temperature between 0 and 2, lower = deterministic
    # top_p is an alternative of temperature, between 0 and 1
  def __api( # messages format: Iterable[ChatCompletionMessageParam]
      self, model, messages, stream=False,
      max_tokens=128, temperature=0.7, top_p=1,
      ) -> ChatCompletion:
    
    # If model passed is not one of the expected ones, print error and end
    if model not in self.__new_models:
      print(f'Unespected newer OpenAI model name: {model}')
      print(f'Available models: {self.__new_models}')
      return
    
    # If is passing a single message
    if type(messages) is str:
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": messages}
        ]
    
    # If everything's ok, call the API
    server_response = self.client.chat.completions.create(
      model=model,
      messages=messages,
      stream=stream,
      max_tokens=128, 
      temperature=0.7, 
      top_p=1
    )

    return server_response

  # Calls OpenAI API for the legacy models and returns the LLM answer
    # If stream == true, function will return stream pointer
    # Otherwise, it will return json object
  def __legacy_api(self, model, prompt) -> ChatCompletion:

    # If model passed is not one of the expected ones, print error and end
    if model not in self.__legacy_models:
      print(f'Unespected legacy OpenAI model name: {model}')
      print(f'Available models: {self.__legacy_models}')
      return
    
    # If everything's ok, call the API
    server_response = self.client.completions.create(
      model=model,
      prompt=prompt
    )
    return server_response

  # Call this function to test Keys and IDs
  def __legacy_test_call(self) -> bool:

    # Make sure the program wont halt by a 
    #   bad api call or unexpected unwrap
    try:

      # Call OpenAI endpoint. All legacy models are free (apparently)
      response = self.__legacy_api(
        model="gpt-3.5-turbo-instruct",
        prompt="Say this is a test!",
      )

      # response = response.choices[0].message.content
      response = response.choices[0].text.strip()
      status = '✅' if response == 'This is a test!' else '⛔'

      # If everything is ok, print and return
      if self.DEBUG_PRINT:
        print(f'{status} Legacy Server response is \'{response}\'')
      return True
    
    except Exception as e:
      # If something's wrong, print and return
      print(e)
      return False
  
  # Call this function to test Keys and IDs, and if paid models are available
  def __test_call(self) -> bool:

    # Make sure the program won't halt by a 
    #   bad api call or unexpected unwrap
    try:

      # Call OpenAI endpoint. Any model works, hence calling the cheapest one
      response = self.__api(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say this is a test!"}],
      )

      # Verify if answer is the default one
      # (and therefore everything works)
      response = response.choices[0].message.content
      status = '✅' if response == 'This is a test!' else '⛔'

      # If everything is ok, print and return
      if self.DEBUG_PRINT:
        print(f'{status} Newer Models Server response is \'{response}\'')
      return True
    
    except Exception as e:
      
      # If something's wrong, print and return
      if self.print_result:
        print(e)
      return False
    
  def run_verification(self):

    # Test legacy models API route
    print("Testing legacy route...")
    legacy_route_result = self.__legacy_test_call()

    # Test newer models API route
    print("Testing newer models route...")
    main_route_result = self.__test_call()

    # Show result
    api_results_ok = legacy_route_result and main_route_result
    print('✅ Everything\'s running!' if api_results_ok else '⛔ Problem detected!')
    

  # Verifies if model selected is new or old, and call functions accordingly
  def single_prompt(self, model: str, prompt: str):

    # If model passed is newer or older model, call API
    if model in self.__new_models:
      response = self.__api(model=model, messages=prompt)
      return response
    elif model in self.__legacy_models:
      response = self.__legacy_api(model=model, prompt=prompt)
      return response
    
    # If unexpected model, print error
    print(f'Unespected OpenAI model name: {model}')
    print(f'Available models: {self.__new_models + self.__legacy_models}')

  def single_prompt_usage_example(self):
    response = self.single_prompt(
      model='gpt-3.5-turbo',
      prompt = "How many rings saturn has and what are their given names?")
    # Printing the response in terminal
    # print(f'Raw: {response}')
    openai_responses = [ x.message.content for x in response.choices]
    print('# Response:') # empty line for visual separation in terminal
    [ print(f'{x}\n') for x in openai_responses ]

  # Verifies if model selected is new or old, and call functions accordingly
  # prompt format: Iterable[ChatCompletionMessageParam]
  def complex_prompt(self, model: str, messages): 

    # If model passed is newer or older model, call API
    if model in self.__new_models:
      response = self.__api(model=model, messages=messages)
      return response
    elif model in self.__legacy_models:
      response = self.__legacy_api(model=model, messages=messages)
      return response
    
    # If unexpected model, print error
    print(f'Unespected OpenAI model name: {model}')
    print(f'Available models: {self.__new_models + self.__legacy_models}')

  def complex_prompt_usage_example(self):
    response = self.complex_prompt(
      model='gpt-3.5-turbo',
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Who won the world series in 2020?"},
          {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
          {"role": "user", "content": "Where was it played?"}
      ],
    )
    # Printing the response in terminal
    # print(f'Raw: {response}')
    openai_responses = [ x.message.content for x in response.choices]
    print('# Response:') # empty line for visual separation in terminal
    [ print(f'{x}\n') for x in openai_responses ]

  def new_long_term_memory(encription_key: str|None):
    # create unique ID
    # create file with said ID
    
    # encript data if encription key is passed
    if encription_key:
      pass

    # return conversation unique id

  # TODO
  def peek(self, conversation_id: str, encription_key: str|None):
    # if conversation already in memory
      # save in main memory the conversation 
      # return conversation
      
    # if conversation not loaded
      # find corresponding file given id
      # read file
      # decript data if encription key was provided
      # save in main memory the conversation
      # return data
    pass

  # TODO
  def long_term_memory(
      self, conversation_id: str, encription_key: str|None,
      model: str,  prompt: str
      ):
    
    # conversation = peek(conversation_id, encription_key)
    # response = self.__api(
      # model,
      # conversation + [{"role": "user", "content": prompt}])
    
    # save data to main memory
    # save data to secondary memory (update file with newest data)

    # return response
    
    pass



