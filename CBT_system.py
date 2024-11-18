import os
from configparser import ConfigParser
from agent.agent_need import CBTAgent, RiskAgent

# Load configuration
config = ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config", "config.ini")
config.read(config_path)

# Extract configurations
BACKGROUND_FILES = {
    "cbt_agent": config.get("Paths", "cbt_agent_background"),
    "risk_agent": config.get("Paths", "risk_agent_background")
}
CONVERSATION_HISTORY_MAX_LENGTH = config.getint("Conversation", "max_history_length")

def main():
    conversation_history = []
    cbt_agent = CBTAgent(BACKGROUND_FILES["cbt_agent"])
    risk_agent = RiskAgent(BACKGROUND_FILES["risk_agent"])

    while True:
        user_prompt = input("You: ")

        # Construct the prompt for CBT Agent
        cbt_prompt = ("Conversation history:\n" + "\n".join(conversation_history) + "\n\n" if conversation_history else "") + \
                     f"Current conversation:\nUser: {user_prompt}\n\nCBT Agent:"
        conversation_history.append(f"User: {user_prompt}")
        cbt_response = cbt_agent.create_response(cbt_prompt)

        # Check for safety with Risk Agent
        risk_prompt = f"""
        User prompt: {user_prompt}
        Talk Agent response: {cbt_response}
        """
        is_safe, reason = risk_agent.respond_check(risk_prompt)

        while not is_safe:
            unsafe_warning = f"""
            User prompt: {user_prompt}
            Original answer: {cbt_response}
            Reason flagged as unsafe: {reason}
            Please regenerate a safe answer.
            """
            cbt_response = cbt_agent.create_response(unsafe_warning)
            is_safe, reason = risk_agent.respond_check(risk_prompt)

        conversation_history.append(f"CBT Agent: {cbt_response}")
        print(f"CBT Agent: {cbt_response}")

        # Trim conversation history if it exceeds max length
        if len(conversation_history) > CONVERSATION_HISTORY_MAX_LENGTH:
            conversation_history = conversation_history[-CONVERSATION_HISTORY_MAX_LENGTH:]

if __name__ == "__main__":
    main()