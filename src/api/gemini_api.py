from google import genai # https://pypi.org/project/google-genai/
from google.genai import types
# print(types.__file__)

import csv
import os
from pathlib import Path
from typing import List, Iterable, Union

'''
To check which models are available, you can use the following URL:
  https://ai.google.dev/gemini-api/docs/models/gemini
And these are the experimental models:
  https://ai.google.dev/gemini-api/docs/models/experimental-models#gemini-api
'''
class GeminiAPI:

  _default_system_prompt = 'You are a helpful assistant.'

  # User model customization
  _max_tokens = 1024
  _temperature = 0.7

  # Save output data in file attributes
  __transpose_data = False # A boolean indicating whether to transpose the CSV outputs (default is False).
  __file_extension = '.csv' # The default file extension for saving CSV files. It currently only accepts csv.

  def __init__(self, API_KEY: str, debug_print: bool = True) -> None:
    self.client = genai.Client(api_key=API_KEY)
    self.debug_print = debug_print

  def __validate_csv_extension(self, file_name: str) -> bool:
    """
    Validates the extension of a file path. If the file does not have a .csv extension, it is added. If the file has a different extension, it is swapped to .csv.

    Parameters:
    - file_path: A string representing the file path.

    Returns:
    - str: The validated file path with the .csv extension.
    """
    # Get the file extension
    _, file_extension = os.path.splitext(file_name)

    # If the file has .csv extension, return the path as it is
    if file_extension.lower() == '.csv':
        return file_name
    # If the file has another extension, print a warning and swap it to .csv
    elif file_extension:
        print("WARNING: Bad file extension passed. Changed to .csv.")
        return os.path.splitext(file_name)[0] + '.csv'
    # If the file has no extension, add .csv
    else:
        return file_name + '.csv'

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
      
      # If there is already a path with this name, don't replace it, but add a number to the end
      aux = 0
      temp_path = file_path + self.__file_extension
      while os.path.exists(temp_path):
        aux += 1
        temp_path = f'{file_path} ({aux}){self.__file_extension}'
      file_path = temp_path
      
      # Format the file path to the configured extension
      if self.__file_extension == '.csv':
        file_path = self.__validate_csv_extension(file_path)
      elif self.__file_extension == '.json':
        pass # TODO: implement json saving
      # file_path = self.__validate_extension(file_path) # it should auto detect the extension and fix it if needed

      # Transpose the data (list of tuples)
      transposed_data = list(zip(*data)) if self.__transpose_data else data

      if self.debug_print:
        print(f"Saving the data to {file_path}")

      # Write the transposed data to the CSV file
      with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(transposed_data)


  def query(self, model: str, prompt: str, system_prompt: str = None) -> str:
    """
    Generates a response from a language model based on the given prompt.

    Parameters:
    - model (str): The name or identifier of the language model to be used.
    - prompt (str): The user input or query for the model.
    - system_prompt (str, optional): A system-level instruction to guide the model's behavior. 
      Defaults to the instance's default system prompt.

    Returns:
    - str: The generated response text from the model.
    """
    if system_prompt is None:
      system_prompt = self._default_system_prompt
    
    response = self.client.models.generate_content(
      model=model, 
      contents=prompt,
      config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=self._max_tokens,
        temperature=self._temperature,
      )
    )
    
    return response.text

  def configure(self, max_tokens: int = 1024, temperature: float = 0.7) -> None:
    """
    Configures the maximum output tokens and temperature for the model responses.

    Parameters:
    - max_tokens (int, optional): The maximum number of tokens the model can generate. Defaults to 1024.
    - temperature (float, optional): The randomness level of the model's responses. 
      Higher values make responses more creative, while lower values make them more deterministic. Defaults to 0.7.
    """
    self._max_tokens = max_tokens
    self._temperature = temperature

  def multiple_queries(self,
    model: str, prompts: List[str], system_prompt: str=None,
    save: bool=False, filename: str=None, filepath: str=None,
    query_simple_questions: List[str]=None) -> List[str]:
    """
    Sends multiple queries to the language model and optionally saves the results.

    Parameters:
    - model (str): The name or identifier of the language model to be used.
    - prompts (List[str]): A list of prompts to send to the model.
    - system_prompt (str, optional): A system-level instruction to guide the model's behavior. Defaults to None.
    - save (bool, optional): If True, saves the output to a CSV file. Defaults to False.
    - filename (str, optional): The name of the file to save the results. Required if 'save' is True.
    - filepath (str, optional): The directory path where the file should be saved. Required if 'save' is True.
    - query_simple_questions (List[str], optional): An alternative set of questions to use as labels for the results. Defaults to the provided prompts.

    Returns:
    - List[Tuple[str, str]]: A list of tuples, where each tuple contains a prompt (or question) and its corresponding response.
    """


    replies = []
    # for text in prompts:
    #   replies.append(self.query(model, text, system_prompt))
    replies = [
      [1, 2],
      [1, 2],
      [1, 2],
    ]

    # Zips the prompts, save the result as a csv file, and return it
    questions = query_simple_questions if query_simple_questions else prompts
    result =  zip(questions, replies)
    if save:
      self.__save_as_csv(result, filename, filepath)

    return result
