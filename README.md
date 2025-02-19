
# LLM Endpoints

This is a small project to help use different LLMs without having to understand their API.
Currently, OpenAI and Google models can be used thorugh this repository.

## How to run

There are 3 main steps needed to run the project.

### Getting necessary keys

After downloading the repository, create a ```.env``` file inside the project folder (```./LLLM-Endpoints/.env```).

For ChatGPT, go to [OpenAI playground](https://platform.openai.com/playground), login, create and save in the ```.env``` file your API Key AND the Octera Organization Identifier.

```
OPENAI_API_KEY=<your-key-here>
OPENAI_ORGANIZATION_ID=<your-new-organization-key-here>
```

For Gemini, go to [Google's AIStudio](https://aistudio.google.com/apikey), login, create and save in the `.env` file your API key.
```
GEMINI_API_KEY=<your-key-here>
```

Once that is done, you are ready to make requests to the selected models.


### Venv Set Up

First, run the virtual environment (venv) and download the necessary packages:

(warning: some packages will freeze the terminal for a few seconds – as long as it doesn't take more than 1 minute, everything is ok and there's no need to exit and restart)

<!-- ✅ New Set up -->
```
source llm-api-venv/bin/activate
pip install -e .
```
If a problem occurs, odds are is that you need to run and `pip install --upgrade pip setuptools wheel`. If this doesn't work, open a new issue, or contact one of the developers.

<!-- ⚠️ Deprecated set-up. Will be deleted on a new version.
```
source llm-api-venv/bin/activate
python setup.py install
``` -->

You can deactivate a virtual environment by typing deactivate in your shell
```
deactivate
```

### Running Inside Venv

The software is pre-loaded with a test using ChatGPT to verify if everything is running accordingly.
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

If you receive something else, make sure your account API key was added to the `.env` file, and that you have permission from OpenAI to use their API. If both are ok, either the packages in the repository are outdated and require maintenance, or some step of the setup was skipped.

### Documentation For Different Models

| Company | Model | Repository Documentation | Official Documentation | Status |
|----------|----------|----------|----------|----------|
| OpenAI | ChatGPT | [open-ai.md](./model-documentation/open-ai.md) | [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction) | ✅ |
| Google | Gemini | [gemini.md](./model-documentation//google-gemini.md) | [Gemini API Docs](https://ai.google.dev/gemini-api/docs) | ✅ |
| DeepSeek AI | DeepSeek | [deepseek.md](./model-documentation/deep-seek.md) | [DeepSeek API Docs](https://api-docs.deepseek.com/) | To be done |


### Troubleshooting
If for some reason the setup is not downloading the necessary files and you're getting errors like ``, you can try the following:

1. Uninstall and Reinstall problematic packages

If you're, for example, getting a `ModuleNotFoundError: No module named 'google.ai'`, try running the following:

```
pip uninstall google-generativeai -y && pip install google-generativeai==0.8.4
```

If the problem is with the openai package:
```
pip uninstall openai -y && pip install openai==1.60.1
```

You can find the package name and versions in the `pyproject.toml` file.

⚠️ This solution was necessary from `setup.py` not being the best scenario anymore, because ["all direct invocations of setup.py are effectively deprecated"](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html). This error should not occur anymore with the current implementation.

2. Reset venv packages:

Here, the problem lies in the venv getting confused with existing packages in the environment, therefore we will clean it and then do a fresh install. The steps are:

* Make sure you are running the venv. If unsure, run: `source llm-api-venv/bin/activate`
* Uninstall packages: `pip freeze | xargs pip uninstall -y`
* If you want to confirm if it uninstalled it all, you can check running `pip list` and see the outputed list
* Run the set up again with `pip install -e .` (include the dot). It will take a couple minutes to fresh install everything.
* If you want, you can run `pip list` to check all installed packages.


### Todo:
- [ ] Conversation with memory, one request at a time
- [ ] Conversation with memory, multiple requests at a time
- [ ] [Test and fix the stream feature](https://cookbook.openai.com/examples/how_to_stream_completions)
- [ ] Consider if conversations should be saved using an encryption key
<!-- - [ ] Separate file storage to it's own class -->

#### Ongoing
- [ ] DeepSeek access
