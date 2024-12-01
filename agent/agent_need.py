import json
from agent.agent import Agent
from pydantic import BaseModel

#-------------------------CBTAgent------------------------------

class CBTAgent(Agent):
    """
    CBT Agent for generating user-focused responses.
    """
    def __init__(self, background_file="cbt_agent_background.txt"):
        super().__init__(background_file)

#-------------------------RiskAgent------------------------------

class RiskAgent_respond_agent(BaseModel):
    '''
    examples:
        {
            "if_safe": false,
            "last_response_role": "patient",
            "reasoning": "The patient expressed suicidal ideation with the statement, 'I don't want to live anymore,' indicating a need for immediate medical intervention."
        }
    '''
    if_safe: bool
    last_response_role: str
    reasoning: str

class BehavioralInterventionPlan(BaseModel):
    weekly_meal_plan: str
    exposure_therapy: str
    body_image_restructuring: str
    behavioral_monitoring: str

class ProfileAgent_plan(BaseModel):
    cognitive_restructuring_plan: str
    behavioral_intervention_plan: BehavioralInterventionPlan

class ProfileAgent_respond_format(BaseModel):
    summary_of_info : str
    plan: ProfileAgent_plan

class RiskAgent(Agent):
    """
    Risk Agent for evaluating safety of interactions.
    """
    def __init__(self, background_file="risk_agent_background.txt", format_output=RiskAgent_respond_agent):
        super().__init__(background_file, format_output)

    def respond_check(self, prompt):
        self.create_response(prompt)
        try:
            self.current_respond = json.loads(self.current_respond)
            if_safe = self.current_respond['if_safe']
            last_response_role = self.current_respond['last_response_role']
            reasoning = self.current_respond['reasoning']
            return if_safe, last_response_role, reasoning
        except ValueError:
            return False, last_response_role, "Response format invalid for risk evaluation."
        
#-------------------------ProfileAgent------------------------------

class ProfileAgent(Agent):
    """
    CBT Agent for generating user-focused responses.
    """
    def __init__(self, background_file="profile_agent_background.txt", format_output=ProfileAgent_respond_format):
        super().__init__(background_file, format_output)