from setuptools import setup, find_packages

setup(
    name='LLM API Endpoints',
    version='0.1.0',
    author='Luiz Pedro Franciscatto Guerra',
    packages=find_packages(),
    install_requires=[
        'python-dotenv==1.0.1',
        'openai==1.12.0',
    ],
)
