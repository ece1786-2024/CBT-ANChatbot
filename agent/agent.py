import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = ""
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
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: Background file '{file_path}' not found.")
            return ""

    def create_response(self, prompt):
        """
        Generate a response based on the agent's background and the given prompt.
        """
        response = client.chat.completions.create(
            model="gpt-4", # changing GPT
            messages=[
                {"role": "system", "content": self.background},
                {"role": "user", "content": prompt},
            ]
        )
        self.current_respond = response.choices[0].message.content
        return self.current_respond