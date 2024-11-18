from agent.agent_need import CBTAgent, RiskAgent

def main():
    conversation_history = []
    cbt_agent = CBTAgent("cbt_agent_background.txt")
    risk_agent = RiskAgent("risk_agent_background.txt")

    while True:
        user_prompt = input("You: ")
        cbt_prompt = ("Conversation history:\n" + "\n".join(conversation_history)) if conversation_history else ""+ \
                     ("Current conversation:\n" + "User: {user_prompt}") + "\n\nCBT Agent:"
        conversation_history.append(f"User: {user_prompt}")
        cbt_response = cbt_agent.create_response(cbt_prompt)
        is_safe, reason = risk_agent.respond_check(cbt_response)
        
        while not is_safe:
            unsafe_warning = f"""
            user prompt: {user_prompt}
            your answer: {cbt_response}
            your answer is not safe and might influence the patient for the reason of: {reason}
            please regenerate a answer please!
            """
            cbt_response = cbt_agent(unsafe_warning)
            is_safe, reason = risk_agent.respond_check(cbt_response)
            
        conversation_history.append(f"CBT Agent: {cbt_response}")
        print(f"CBT Agent: {cbt_response}")

if __name__ == "__main__":
    main()
