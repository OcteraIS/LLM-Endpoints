# Class OpenAI_OrganizationAPI Documentation

## Index

1. [Initialization](#initialization)
1. [Test](#test)
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION_ID = os.getenv("OPENAI_ORGANIZATION_ID")
```

Initializing the object

```python
openai_api = OpenAI_OrganizationAPI(
    OPENAI_API_KEY,
    OPENAI_ORGANIZATION_ID,
    debug_print=True
)
```


## Test

If you wish to test if everything is working, you might want to run the following line. It will automatically print in the terminal the output.
```
openai_api.run_verification()
```

## Usage


### Making requests

There are 4 main methods implemented and all calls default to ```gpt-3.5-turbo```. The answer comes in one single chunk.

#### No-memory requests

To run prompts without long-term memory of any conversation. It comes in two flavors:


##### One request

Sends a single request given a prompt to the model. 


```python
query(
    prompt: str, 
    model: str = 'gpt-3.5-turbo'
) -> list[str]:
```

##### Multiple requests

For each prompt passed, the function will call the API to get the reply and save the answer into a ```.csv``` file, with the first row being the prompts, and the second row being the reply.

Comes in two flavors (single or multi-threaded), and returns a string tuple array, containing pairs of prompts and their corresponding replies formatted as ```(prompt, reply)```

```python
# Runs all prompts sequentially
single_thread_queries(
    prompts: list[str], 
    system_prompt: Union[str, None] = None, 
    model: str = 'gpt-3.5-turbo',
    query_output_path: str = None, 
    query_output_filename: str = 'result'
) -> zip

# Runs all prompts concurrently
multi_thread_queries(
    prompts: list[str], 
    system_prompt: Union[str, None] = None, 
    model: str = 'gpt-3.5-turbo', 
    query_output_path: str = None, 
    query_output_filename: str = 'result'
) -> list[str, str]
```

#### Memory requests

Allows the user to talk with the model via the terminal/have access to long term memory. This section is still being explored.

<!-- complex_prompt(model, prompt)
#### new_long_term_memory(model, prompt)
#### long_term_memory(model, prompt)
#### peek(model, prompt) -->


### Changing model parameters

There are multiple parameters a LLM can use. The ones currently supported are:

- ```stream```: A boolean indicating whether to stream responses or not (default is False).
- ```max_tokens```: An integer representing the maximum number of tokens to generate (default is 128).
- ```temperature```: A float representing the sampling temperature for generating responses (default is 0.7).
- ```top_p```: A float representing the nucleus sampling parameter (default is 1).

```python
set_model_parameters(
    stream: bool = False, 
    max_tokens: int = 128, 
    temperature: float = 0.7, 
    top_p: float = 1
) -> None
```