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
        self.risk_times = 0

    def respond_check(self, prompt):
        self.create_response(prompt)
        lines = self.current_respond.split("\n")
        if len(lines) >= 1 and "Risk Level:" in lines[0]:
            first_line = lines[0].strip()
            try:
                risk_level_part, reason_part = first_line.split(",", 1)
                risk_level = risk_level_part.split(":")[1].strip()
                reason = reason_part.split("Reason:")[1].strip()
            except ValueError:
                risk_level = "Unknown"
                reason = "Parsing error in the first line"
        else:
            risk_level = "Unknown"
            reason = "Missing first line"

        # Parse the second line for response (empty for Low Risk)
        if len(lines) >= 2:
            response = lines[1].strip()
        else:
            response = ""

        return risk_level, reason, response
