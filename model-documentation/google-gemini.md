# Class GeminiAPI Documentation

## Index

1. [Initialization](#initialization)
1. [Usage](#usage)
  1. [Making requests](#making-requests)
    1. [No-memory requests](#no-memory-requests)
      1. [One request](#one-request)
      1. [Multiple requests](#multiple-requests)
    1. [Memory requests](#memory-requests)
  1. [Changing model parameters](#changing-model-parameters)


## Initialization

Loading the keys from the `.env` file

```python
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

Initializing the object

```python
gemini_api = GeminiAPI(GEMINI_API_KEY, debug_print=True)
```

## Usage

### Making requests

There are two primary methods for making requests to the model.

#### Single query

Sends a single request to the model and retrieves a response.

```py
query(
    model: str,
    prompt: str,
    system_prompt: str = None
) -> str
```

Example usage:

```py
response = custom_model.query("gpt-3.5-turbo", "What is the capital of France?")
print(response)
```

#### Multiple queries

Processes multiple prompts and retrieves responses for each. Optionally, results can be saved to a CSV file.

```py
multiple_queries(
    model: str,
    prompts: list[str],
    system_prompt: str = None,
    save: bool = False,
    filename: str = None,
    filepath: str = None,
    query_simple_questions: list[str] = None
) -> list[tuple[str, str]]
```

Example usage:

```py
prompts = ["What is AI?", "How does deep learning work?"]
responses = custom_model.multiple_queries("gpt-3.5-turbo", prompts, save=True, filename="results.csv")
print(responses)
```

If save=True, results will be stored as a CSV file, with each row containing a prompt and its corresponding response

The `query_simple_questions` attribute is an alternative set of questions to use as labels when saving the results. Defaults to the provided prompts. 
  This is important when running multiple prompts that are similar to eachother but have small differences, and this attribute allows the saved csv to only contain the differences to make it easier to read.

### Changing model parameters

Modify model configuration, such as token limit and temperature, to control response behavior.

```py
configure(
    max_tokens: int = 1024,
    temperature: float = 0.7
) -> None
```

Example usage:

```py
custom_model.configure(max_tokens=512, temperature=0.5)
```

This allows customization of the output length and response creativity.