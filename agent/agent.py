import os
from openai import OpenAI
from configparser import ConfigParser

# Load configuration
config = ConfigParser()

# Specify the path to the config file
config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.ini")
config.read(config_path)

OPENAI_API_KEY = config.get("OpenAI", "api_key")
OPENAI_MODEL = config.get("OpenAI", "model")

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), 
)

class Agent:
    """
    Base class for agents.
    """
    def __init__(self, background_file):
        self.current_respond = ""
        self.background = self.load_background(background_file)

    def load_background(self, file_path):
        """
        Load the background knowledge from a text file.
        """
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: Background file '{file_path}' not found.")
            return ""

    def create_response(self, prompt):
        """
        Generate a response based on the agent's background and the given prompt.
        """
        response = client.chat.completions.create(
            model=OPENAI_MODEL, # changing GPT
            messages=[
                {"role": "system", "content": self.background},
                {"role": "user", "content": prompt},
            ]
        )
        self.current_respond = response.choices[0].message.content
        return self.current_respond