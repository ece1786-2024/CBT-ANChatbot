from agent.agent import Agent

class CBTAgent(Agent):
    """
    CBT Agent for generating user-focused responses.
    """
    def __init__(self, background_file="cbt_agent_background.txt"):
        super().__init__(background_file)

class RiskAgent(Agent):
    """
    Risk Agent for evaluating safety of interactions.
    """
    def __init__(self, background_file="risk_agent_background.txt"):
        super().__init__(background_file)

    def respond_check(self, prompt):
        self.create_response(prompt)
        check, reason = self.current_respond.split(' ', 1)
        return check.lower() == "safe", reason