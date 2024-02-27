
# LLM Endpoints

This is a small project to help using different LLMs without having to understand their API.
Currently, only OpenAI models are working.

## OpenAI

There are 3 main steps needed to run the project.

### Getting necessary keys

After downloading the repository, create a ```.env``` file inside the project folder (```./LLLM-Endpoints/.env```).

After trat, go to [OpenAI playground](https://platform.openai.com/playground), login, create and save in the ```.env``` file your API Key AND the Octera Organization Identifier.

```
OPENAI_API_KEY=<your-key-here>
OPENAI_ORGANIZATION_ID=<your-new-organization-key-here>
```

Once that is done, you are ready to do requests to OpenAI API.


### Running the program

First, run the virtual environment (venv) and download the necessary packages:

(warning: there are some packages that will freeze the terminal for a few seconds – as long as it doesn't takes more than 1 minute, everything is ok and there's no need to exit and restart)

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

If you receive something else, either the packages in the repository are outdated and it requires maintenance or some step of the set up was skipped.

### Making requests

There are 4 main methods implemented. The answer comes in one chunk, but if you want to have it streamed (just like how it works in the website), you can. However, this feature is not fully tested and can lead to interesting results.

#### No-memory requests

To run prompts without long-term memory of any conversation. It comes in two flavours:


##### One request

Sends a single request given a prompt to the model:

```python
single_prompt(model: str, prompt: str) -> str
```

##### Multiple requests

For each prompt passed, the function will call the API to get the reply and save the answer into a ```.csv``` file, with the first row being the prompts, and the second row being the reply.

It also returns an string tuple array, containing a list formated as ```(prompt, reply)```

```python
# TO BE IMPLEMENTED
single_prompt(model: str, prompts: [str], output_path: str) -> [(str, str)]
```

#### Memory requests

This section is still beeing explored

<!-- complex_prompt(model, prompt)
#### new_long_term_memory(model, prompt)
#### long_term_memory(model, prompt)
#### peek(model, prompt) -->

### Todo:
- [ ] Properly comment the code
- [ ] Allow to change the (main) system prompt
- [ ] No-memory multiple requests
- [ ] Conversation with memory, one request at a time
- [ ] Conversation with memory, multiple requests at a time
- [ ] Consider if conversations should be saved using an encryption key