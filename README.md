
# LLM Endpoints

This is a small project to help use different LLMs without having to understand their API.
Currently, only OpenAI models are working.

## OpenAI

There are 3 main steps needed to run the project.

### Getting necessary keys

After downloading the repository, create a ```.env``` file inside the project folder (```./LLLM-Endpoints/.env```).

After that, go to [OpenAI playground](https://platform.openai.com/playground), login, create and save in the ```.env``` file your API Key AND the Octera Organization Identifier.

```
OPENAI_API_KEY=<your-key-here>
OPENAI_ORGANIZATION_ID=<your-new-organization-key-here>
```

Once that is done, you are ready to make requests to OpenAI API.


### Running the program

First, run the virtual environment (venv) and download the necessary packages:

(warning: some packages will freeze the terminal for a few seconds – as long as it doesn't take more than 1 minute, everything is ok and there's no need to exit and restart)

```
source llm-api-venv/bin/activate
python setup.py install
```

You can deactivate a virtual environment by typing deactivate in your shell
```
deactivate
```

The software is pre-loaded with a test to verify if everything is running accordingly.
After running the main file:

```
python src/main.py
```

You should see the following message:

```
Testing legacy route...
✅ Legacy Server response is 'This is a test!'
Testing newer models route...
✅ Newer Models Server response is 'This is a test!'
✅ Everything's running!
```

If you receive something else, either the packages in the repository are outdated and require maintenance or some step of the setup was skipped.

### Making requests

There are 4 main methods implemented and all calls default to ```gpt-3.5-turbo```. The answer comes in one chunk, but if you want to have it streamed (just like how it works on the website), you can. However, this feature is not fully tested and can lead to interesting results.

#### No-memory requests

To run prompts without long-term memory of any conversation. It comes in two flavors:


##### One request

Sends a single request given a prompt to the model. 


```python
query(self, prompt: str, model: str = 'gpt-3.5-turbo') -> list[str]:
```

##### Multiple requests

For each prompt passed, the function will call the API to get the reply and save the answer into a ```.csv``` file, with the first row being the prompts, and the second row being the reply.

Comes in two flavors (single or multi-threaded), and returns a string tuple array, containing pairs of prompts and their corresponding replies formatted as ```(prompt, reply)```

```python
# Runs all prompts sequentially
single_thread_queries(self, prompts: list[str], system_prompt: Union[str, None] = None, model: str = 'gpt-3.5-turbo', query_output_path: str = None, query_output_filename: str = 'result') -> zip

# Runs all prompts concurrently
multi_thread_queries(self, prompts: list[str], system_prompt: Union[str, None] = None, model: str = 'gpt-3.5-turbo', query_output_path: str = None, query_output_filename: str = 'result') -> list[str, str]
```

#### Memory requests

This section is still being explored

<!-- complex_prompt(model, prompt)
#### new_long_term_memory(model, prompt)
#### long_term_memory(model, prompt)
#### peek(model, prompt) -->


### Changing models parameters

There are multiple parameters a LLM can use. The ones currently supported are:

- ```stream```: A boolean indicating whether to stream responses or not (default is False).
- ```max_tokens```: An integer representing the maximum number of tokens to generate (default is 128).
- ```temperature```: A float representing the sampling temperature for generating responses (default is 0.7).
- ```top_p```: A float representing the nucleus sampling parameter (default is 1).

```python
set_model_parameters(self, stream: bool = False, max_tokens: int = 128, temperature: float = 0.7, top_p: float = 1) -> None
```


### Todo:
- [X] Properly comment on the code
- [X] Allow to change the (main) system prompt
- [X] No-memory multiple requests
- [X] Conversation with memory, pre-set conversation
- [X] Allow settings (e.g. temperature) in high-level functions
- [X] Save big queries locally in files
- [ ] Conversation with memory, one request at a time
- [ ] Conversation with memory, multiple requests at a time
- [ ] [Test and fix the stream feature](https://cookbook.openai.com/examples/how_to_stream_completions)
- [ ] Consider if conversations should be saved using an encryption key