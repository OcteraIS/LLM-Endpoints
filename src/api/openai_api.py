import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from typing import List, Iterable, Union
from openai import OpenAI, ChatCompletion, Stream
from openai.types.chat import ChatCompletionMessageParam

import csv
import os
from pathlib import Path


class OpenAI_OrganizationAPI:

  # Newest model identifiers
  # endpoint: https://api.openai.com/v1/completions
  # Check available models at https://platform.openai.com/docs/models
  
  # Legacy model identifiers
  # endpoint: https://api.openai.com/v1/chat/completions
  __legacy_models = ['gpt-3.5-turbo-instruct', 'babbage-002', 'davinci-002']

  # Default system prompt
  # Used to coerce the model to perform specific tasks
  __default_system_prompt = 'You are a helpful assistant.'

  # Model parameters
  __stream = False # A boolean indicating whether to stream responses or not (default is False).
  __max_tokens = 256 # An integer representing the maximum number of tokens to generate (default is 256).
  __temperature = 0.7 # A float representing the sampling temperature for generating responses (default is 0.7).
  __top_p = 1 # A float representing the nucleus sampling parameter (default is 1).
  __transpose_data = False # A boolean indicating whether to transpose the CSV outputs (default is False).

  def __init__(self, API_KEY: str, ORGANIZATION_ID: str, debug_print: bool = True) -> None:
    """
      Initializes OpenAI_OrganizationAPI with the provided API_KEY, ORGANIZATION_ID, and debug_print settings.
      Automatically handles synchronous OpenAI client calls through a proprietary instance

      Parameters:
      - API_KEY: A string representing the API key.
      - ORGANIZATION_ID: A string representing the organization ID.
      - debug_print: A boolean indicating whether debug information should be printed (default is True).
    """

    self.API_KEY = API_KEY
    self.ORGANIZATION_ID = ORGANIZATION_ID

    self.client = OpenAI(
      organization=ORGANIZATION_ID,
      api_key=API_KEY
    )

    self.DEBUG_PRINT = debug_print
  
  # MARK: Private functions

  # Helper functions
    
  def __remove_quotes(self, text) -> str:
    """
    Removes leading and trailing single or double quotes from a string.
    This is here because sometimes the LLM returns text with extra quotes, making validation harder

    Parameters:
    - text (str): The input string that is possibly enclosed in single or double quotes.

    Returns:
    - str: The input string with leading and trailing quotes removed, if present.
    """
    while text.startswith('"') or text.startswith("'") :
        text = text[1:]
    while text.endswith('"') or text.endswith("'"):
        text = text[:-1]
    return text

  def __correct_input_pattern(self, json_obj: list[tuple[str, str]]) -> bool:
    """
    Verifies if a list of tuples representing conversational roles follows a specific pattern.

    Each tuple in the list should have the first element as 'user' or 'assistant',
    and the second element is the corresponding content.
    The first tuple should start with 'user', and the last one should end with 'user'.

    Parameters:
    - json_obj (List[Tuple[str, str]]): The list of tuples representing alternating conversational roles. The expected format is:
    [
      ("user", "Who won the World Series in 2020?"),
      ("assistant", "The Los Angeles Dodgers won the World Series in 2020."),
      ("user", "Where was it played?")
    ]

    Returns:
    - bool: True if the list of tuples follows the pattern, False otherwise.
    """
    if not json_obj:
      return False
    
    # Iterate through the list starting from the second element
    for i in range(1, len(json_obj)):
        # Check if the current element is equal to the previous one
        if json_obj[i] == json_obj[i - 1]:
            return False  # Return False if two consecutive elements are equal

    # Check if the first tuple starts with 'user' and the last one ends with 'user'
    if json_obj[0][0] != 'user' or json_obj[-1][0] != 'user':
      return False

    return True
  
  def __map_formatted_texts_to_openai_message(self, tuple_list: list[tuple[str, str]], system_prompt: Union[None, str]) -> List[dict]:
    """
    Maps a list of tuples representing conversational roles to a list of dictionaries.

    Parameters:
    - tuple_list (List[Tuple[str, str]]): The list of tuples representing conversational roles.
    - system_prompt (str): A string representing the system prompt for the model. Defaults to 'You are a helpful assistant'.

    Returns:
    - List[dict]: The list of dictionaries with keys 'role' and 'content'.
    """

    if not system_prompt:
      system_prompt = self.__default_system_prompt

    dict_list = [
       {"role": "system", "content": system_prompt}
    ]

    for role, content in tuple_list:
        dict_list.append({"role": role, "content": content})
    return dict_list

  def __map_text_to_openai_message(
      self,
      text_input: Union[str, list[str]],
      system_prompt: Union[None, str]
      ) -> List[dict[str, str]]:
    """
    Maps a list of text prompts to a list of dictionaries representing conversational roles.
    If multiple messages are passed, this returns multiple single message objects, for each to be used separately.

    Parameters:
    - input (Union[str, List[str]]): Either a string or a list of strings representing text prompts.
    - system_prompt (Union[None, str]): The system prompt to use. If None, defaults to "You are a helpful assistant."

    Returns:
    - List[dict]: A list of dictionaries with keys 'role' and 'content'.
    """

    if not system_prompt:
      system_prompt = self.__default_system_prompt

    system_prompt_format = {"role": "system", "content": system_prompt}

    # If the input is a string
    if type(text_input) == str:
      return [system_prompt_format, {"role": "user", "content": text_input} ]
    
    # If the input is a list of strings
    return [ [system_prompt_format, {"role": "user", "content": text} ] for text in text_input]

  def __validate_csv_extension(self, file_path: str) -> str:
    """
    Validates the extension of a file path. If the file does not have a .csv extension, it is added. If the file has a different extension, it is swapped to .csv.

    Parameters:
    - file_path: A string representing the file path.

    Returns:
    - str: The validated file path with the .csv extension.
    """
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # If the file has .csv extension, return the path as it is
    if file_extension.lower() == '.csv':
        return file_path
    # If the file has another extension, print a warning and swap it to .csv
    elif file_extension:
        print("WARNING: Bad file extension passed. Changed to .csv.")
        return os.path.splitext(file_path)[0] + '.csv'
    # If the file has no extension, add .csv
    else:
        return file_path + '.csv'

  def __save_as_csv(self, data: list[tuple[str,str]], filename: str, download_path: str = None) -> None:
    """
    Save a list of tuples as a CSV file.

    Parameters:
    - data: A list of tuples to be saved as a CSV file.
    - filename: A string representing the filename for the CSV file.
    - custom_path: A string representing the custom path for saving the CSV file (default is Downloads folder).

    Returns:
    - None
    """

    # Create the full path to the CSV file
    if download_path:

      if os.path.exists(download_path):
        file_path = os.path.join(download_path, filename)
      else:
        print('WARNING: Invalid path given. Saving to downloads folder istead.')
        file_path = str(Path.home() / "Downloads")

    else:
      # If no custom path is given, save to the downloads folder
      file_path = os.path.join(
        (str(Path.home() / "Downloads")),
        filename
      )

    # Format the file path to csv
    file_path = self.__validate_csv_extension(file_path)

    # Transpose the data (list of tuples)
    transposed_data = list(zip(*data)) if self.__transpose_data else data

    # Write the transposed data to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile)
      csv_writer.writerows(transposed_data)


  # Open AI API functions

  def __api(self, model: str, messages: List[dict[str, str]]) -> ChatCompletion:
    """
    Calls the API for chat completion using the provided parameters.

    Parameters:
    - model: A string representing the model to be used for chat completion.
    - messages: A list of dictionaries (defined by OpenAI themselves) providing additional parameters for each message.
    - stream: A boolean indicating whether to stream responses or not (default is False).
    - max_tokens: An integer representing the maximum number of tokens to generate (default is 128).
    - temperature: A float representing the sampling temperature for generating responses (default is 0.7).
    - top_p: A float representing the nucleus sampling parameter (default is 1).

    Returns:
    - ChatCompletion: An object containing the response stream from the API.
    """
    
    # If everything's ok, call the API
    server_response = self.client.chat.completions.create(
      model=model,
      messages=messages,
      stream=self.__stream,
      max_tokens=self.__max_tokens, 
      temperature=self.__temperature, 
      top_p=self.__top_p
    )

    return server_response

  def __legacy_api(self, model: str, prompt: List[dict[str, str]]) -> Union[ChatCompletion, dict]:
    """
      Calls the OpenAI API for the legacy models and returns the LLM answer.

    Parameters:
    - model: A string representing the legacy model to be used.
    - prompt: A string representing the prompt for the model.
    - stream: A boolean indicating whether to return a stream pointer if true,
              otherwise return a JSON object (default is False).

    Returns:
    - Union[ChatCompletion, dict]: If stream is true, the function returns a stream pointer,
                                    otherwise, it returns a JSON object.
    """

    # If the model passed is not one of the expected ones, print error and end
    if model not in self.__legacy_models:
      print(f'Unespected legacy OpenAI model name: {model}')
      print(f'Available models: {self.__legacy_models}')
      return
    
    # If everything's ok, call the API
    server_response = self.client.completions.create(
      model=model,
      prompt=prompt,
      stream=self.__stream
    )
    return server_response

# Call this function to test Keys and IDs, and if paid models are available
  def __test_call(self) -> bool:
    """
    Performs a test call to the newer models API rout system and returns True if successful, False otherwise.

    Returns:
    - bool: True if the test call is successful, False otherwise.
    """

    # Make sure the program won't halt by a  bad API call or unexpected unwrap
    try:

      # Call OpenAI endpoint. Any model works, hence calling the cheapest one
      response = self.__api(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say this is a test!"}],
      )

      # Verify if the answer is the default one
      # (and therefore everything works)
      response: str = self.__remove_quotes(response.choices[0].message.content)
      status = '✅' if response == 'This is a test!' else '⛔'

      # If everything is ok, print and return
      if self.DEBUG_PRINT:
        print(f'{status} Newer Models Server response is \'{response}\'')
      return True
    
    except Exception as e:
      
      # If something's wrong, print and return
      if self.DEBUG_PRINT:
        print(e)
      return False
  
  def __legacy_test_call(self) -> bool:
    """
    Performs a test call to the legacy system and returns True if successful, False otherwise.

    Returns:
    - bool: True if the test call is successful, False otherwise.
    """

    # Make sure the program won't halt by a bad API call or unexpected unwrap
    try:

      # Call OpenAI endpoint. All legacy models are free (apparently)
      response = self.__legacy_api(
        model="gpt-3.5-turbo-instruct",
        prompt="Say this is a test!",
      )

      # response = response.choices[0].message.content
      response: str = self.__remove_quotes(response.choices[0].text.strip())

      status = '✅' if response == 'This is a test!' else '⛔'

      # If everything is ok, print and return
      if self.DEBUG_PRINT:
        print(f'{status} Legacy Server response is \'{response}\'')
      return True
    
    except Exception as e:
      # If something's wrong, print and return
      print(e)
      return False

  # MARK: Public functions
    
  def configure(self, stream: bool = False, max_tokens: int = 128, temperature: float = 0.7, top_p: float = 1, transpose_csv_outputs: str = False)-> None:
    # Redundant function for easier use
    self.set_model_parameters(stream, max_tokens, temperature, top_p, transpose_csv_outputs)

  def set_model_parameters(self, stream: bool = False, max_tokens: int = 128, temperature: float = 0.7, top_p: float = 1, transpose_csv_outputs: str = False) -> None:
    """
    Sets the parameters for the model.

    Parameters:
    - stream: A boolean indicating whether to stream responses or not (default is False).
    - max_tokens: An integer representing the maximum number of tokens to generate (default is 128).
    - temperature: A float representing the sampling temperature for generating responses (default is 0.7).
    - top_p: A float representing the nucleus sampling parameter (default is 1).
    - transpose_csv_outputs: A boolean indicating whether to transpose the CSV outputs (default is False). If True, each line in the csv will be a prompt and its corresponding reply, otherwise, one column will be prompts and the other will be replies.

    Returns:
      - None
    """

    # Verifies if temperature or top_p are being updated, if both: warn it, else, keep going
    if temperature != 0.7 and top_p != 1:
      print("Warning: Please only change either temperature or top_p, not both.")

    self.__stream = stream
    self.__max_tokens = max_tokens
    self.__temperature = temperature
    self.__top_p = top_p

  def run_verification(self):
    """
    Runs verification tests for both legacy and newer models API routes and displays the results.
    """

    # Test legacy models API route
    print("Testing legacy route...")
    legacy_route_result = self.__legacy_test_call()

    # Test newer models API route
    print("Testing newer models route...")
    main_route_result = self.__test_call()

    # Show result
    api_results_ok = legacy_route_result and main_route_result
    print('✅ Everything\'s running!' if api_results_ok else '⛔ Problem detected!')
  # Is not supporting stream methods yet

  def query(self, prompt: str, system_prompt: Union[str, None] = None, model: str = 'gpt-3.5-turbo') -> list[str]:
    """
    Processes a single prompt with the specified model and returns the result.

    Parameters:
    - prompt: A string representing the prompt to be processed.
    - system_prompt (Union[None, str]): The system prompt to use. If None, defaults to "You are a helpful assistant."
    - model: A string representing the model to be used for processing the prompt. Defaults to gpt-3.5-turbo

    Returns:
    - list[str]: The result of processing the prompt. It is a list because it may return more than one reply.
    """

    # If the model passed is an older model, call API
    if model in self.__legacy_models:
      response = self.__legacy_api(model=model, prompt=prompt)
      return [choice.text for choice in response.choices] 
    
    # If model passed is a new one, call new models API endpoint
    # Check available models at https://platform.openai.com/docs/models
    response = self.__api(model=model, messages=self.__map_text_to_openai_message(prompt, system_prompt=system_prompt))
    return [ choice.message.content for choice in response.choices]

  def single_thread_queries(self, prompts: list[str], system_prompt: Union[str, None] = None, model: str = 'gpt-3.5-turbo', query_output_path: str = None, query_output_filename: str = 'result') -> zip:
    """
    Processes a list of prompts with the specified model and returns a zip of prompts and replies.
    Saves output to file.

    Parameters:
    - prompts: A list of strings representing the prompts to be processed.
    - system_prompt (Union[None, str]): The system prompt to use. If None, defaults to "You are a helpful assistant."
    - model: A string representing the model to be used for processing the prompts (default is 'gpt-3.5-turbo').
    - query_output_path: A string representing the custom path for saving the CSV file (default is Downloads folder).
    - query_output_filename: A string representing the filename for the CSV file.

    Returns:
    - zip: A zip object containing pairs of prompts and their corresponding replies.
    """
    _total = len(prompts)
    _count = 1

    replies = []
    for text in prompts:
      replies.append(self.query(text, system_prompt, model))

      if self.DEBUG_PRINT:
        print(f'Completed query: {_count} out of {_total}.')
        _count += 1

    result =  zip(prompts, replies)
    self.__save_as_csv(result, query_output_filename, query_output_path)
    return result
  
  def multi_thread_queries(self, prompts: list[str], system_prompt: Union[str, None] = None, model: str = 'gpt-3.5-turbo', query_output_path: str = None, query_output_filename: str = 'result') -> list[str, str]:
    """
    Executes multiple queries concurrently using threads.
    Saves output to file.

    Parameters:
    - prompts (list[str]): A list of text prompts for which queries need to be made.
    - system_prompt (Union[None, str]): The system prompt to use. If None, defaults to "You are a helpful assistant."
    - model (str): The model used for querying.
    - query_output_path: A string representing the filename for the CSV file.
    - query_output_filename: A string representing the custom path for saving the CSV file (default is Downloads folder).

    Returns:
    - list[str, str]: A list containing pairs of prompts and their corresponding replies.
    """
    # Append functions are atomic, therefore in this case it is fine to use a generic list
    # Look at https://docs.python.org/3/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe
    replies = []
    
    # Use ThreadPoolExecutor to execute query_thread concurrently
    with ThreadPoolExecutor() as executor:
        # Submit each query to the thread pool
        future_to_text = {executor.submit(self.query, text, system_prompt, model): text for text in prompts}
        
        # Gather results as they complete
        for future in concurrent.futures.as_completed(future_to_text):
            text = future_to_text[future]
            try:
                reply = future.result()
                replies.append((text, reply))
            except Exception as exc:
                print(f'Query for "{text}" generated an exception: {exc}')
    
    # Once all threads ended, return results
    self.__save_as_csv(replies, query_output_filename, query_output_path)
    return replies

  def multi_turn_query(self, messages: list[tuple[str, str]], system_prompt: Union[None, str] = None, model: str = 'gpt-3.5-turbo') -> Union[None, str]:
    """
    Performs a multi-turn query using a conversational model.
    Does not save output to file.

    Parameters:
    - messages (List[Tuple[str, str]]): A list of tuples representing conversational turns.
      Each tuple should contain a role ('user' or 'assistant') and content.
    - system_prompt (Union[None, str]): The system prompt to use. If None, defaults to "You are a helpful assistant."
    - model (str): The name of the model to use for the query. Defaults to 'gpt-3.5-turbo'.

    Returns:
    - Union[None, str]: The response from the API if the model is recognized, otherwise None.
    """
    
    # Verify if the input passed follows the correct pattern
    if not self.__correct_input_pattern(messages):
      print('Memory input in invalid format. Expected format:')
      print(
        """
        [
          ("user", "Who won the World Series in 2020?"),
          ("assistant", "The Los Angeles Dodgers won the World Series in 2020."),
          ("user", "Where was it played?")
        ]
        """
      )
      return
    
    if not system_prompt:
      system_prompt = self.__default_system_prompt

    json_body = self.__map_formatted_texts_to_openai_message(messages, system_prompt)

    # If the model passed is a newer or older model, call API
    
    # FIXME: Legacy route not working here
    if model in self.__legacy_models:
      response = self.__legacy_api(model=model, messages=json_body)
      return json_body + [choice.text for choice in response.choices]
    
    # Check available models at https://platform.openai.com/docs/models
    response = self.__api(model=model, messages=json_body)
    texts = [ choice.message.content for choice in response.choices]
    texts = texts if len(texts) > 1 else texts[0]
    return json_body + [{"role":"user", "content":texts}]


"""
===============================
Newer models JSON reply format:
===============================
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo-0125",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "logprobs": null,
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}

=========================
Legacy models JSON reply format:
=========================
{
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "logprobs": null,
      "text": "\n\n\"Let Your Sweet Tooth Run Wild at Our Creamy Ice Cream Shack"
    }
  ],
  "created": 1683130927,
  "id": "cmpl-7C9Wxi9Du4j1lQjdjhxBlO22M61LD",
  "model": "gpt-3.5-turbo-instruct",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 16,
    "prompt_tokens": 10,
    "total_tokens": 26
  }
}

"""


  # TODO: following sections are parts that are still being explored

  # def new_long_term_memory(encription_key: str|None):
  #   # create unique ID
  #   # create file with said ID
    
  #   # encript data if encription key is passed
  #   if encription_key:
  #     pass

  #   # return conversation unique id

  # # TODO
  # def peek(self, conversation_id: str, encription_key: str|None):
  #   # if conversation already in memory
  #     # save in main memory the conversation 
  #     # return conversation
      
  #   # if conversation not loaded
  #     # find corresponding file given id
  #     # read file
  #     # decript data if encription key was provided
  #     # save in main memory the conversation
  #     # return data
  #   pass

  # # TODO
  # def long_term_memory(
  #     self, conversation_id: str, encription_key: str|None,
  #     model: str,  prompt: str
  #     ):
    
  #   # conversation = peek(conversation_id, encription_key)
  #   # response = self.__api(
  #     # model,
  #     # conversation + [{"role": "user", "content": prompt}])
    
  #   # save data to main memory
  #   # save data to secondary memory (update file with newest data)

  #   # return response
    
  #   pass

  # def print_from_stream(stream: Stream):
  #   for chunk in stream:
  #     if chunk.choices[0].delta.content is not None:
  #         print(chunk.choices[0].delta.content, end="")


