import os
import json
from configparser import ConfigParser
from users.login_register import menu
from agent.agent_need import CBTAgent, RiskAgent, ProfileAgent

# Load configuration
config = ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config", "config.ini")
config.read(config_path)

# Extract configurations
BACKGROUND_FILES = {
    "cbt_agent_stage1": config.get("Paths", "cbt_agent_stage1_background"),
    "cbt_agent_stage3": config.get("Paths", "cbt_agent_stage3_background"),
    "risk_agent": config.get("Paths", "risk_agent_background"),
    "profile_agent": config.get("Paths", "profile_agent_background")
}

CONVERSATION_HISTORY_MAX_LENGTH  = config.getint("Conversation", "max_history_length") * 2
CONVERSATION_DURATION_MAX_LENGTH = config.getint("Conversation", "max_conversation_duration_length")
CONVERSATION_ENDING_REMINDER     = config.getint("Conversation","ending_remind")

conversation_history = []

def conversation_structure(risk_agent, cbt_agent, profile):

    global conversation_history
    count = 0

    while count < CONVERSATION_DURATION_MAX_LENGTH:

        user_prompt = input("\nYou: ")

        # Construct the prompt for CBT Agent
        asd = json.dumps(profile)
        aaa = profile["current_session_number"] != 0
        cbt_prompt = ((f"Here is the patient previous data: {asd}") + ("" if aaa else "This is the first time patient been here")) + \
                     (("Conversation history:\n" + "\n".join(conversation_history) + "\n\n") if conversation_history else "") + \
                     f"Current conversation:\nUser: {user_prompt}\n\nCBT Agent:"
        
        if CONVERSATION_DURATION_MAX_LENGTH - count == CONVERSATION_ENDING_REMINDER:
            print(f"\nOnly {CONVERSATION_ENDING_REMINDER} conversations remaining!!!")
            cbt_prompt += "\nSystem info: Only {CONVERSATION_ENDING_REMINDER} conversations remaining!"

        conversation_history.append(f"User: {user_prompt}")

        risk_prompt = f"""
        User prompt: {user_prompt}
        """

        is_safe, last_response_role, reasoning = risk_agent.respond_check(risk_prompt)
        if is_safe:
            cbt_response = cbt_agent.create_response(cbt_prompt)
        else:
            print(f"The conversation is temperary shut down due to:\n{last_response_role} : {reasoning}. Please seek immediate help.")
            break

        # Check for safety with Risk Agent
        risk_prompt = f"""
        CBT Agent response: {cbt_response}
        """

        is_safe, last_response_role, reasoning = risk_agent.respond_check(risk_prompt)

        if is_safe:
            conversation_history.append(f"CBT Agent: {cbt_response}")
            print(f"\nCBT Agent: {cbt_response}")
        else:
            print(f"The conversation is temperary shut down due to:\n{last_response_role} : {reasoning}")
            break

        # Trim conversation history if it exceeds max length
        if len(conversation_history) > CONVERSATION_HISTORY_MAX_LENGTH:
            conversation_history = conversation_history[-CONVERSATION_HISTORY_MAX_LENGTH:]
        count += 1
    # conversation_history.clear()
    
def stage_one(profile):
    cbt_agent  = CBTAgent(BACKGROUND_FILES["cbt_agent_stage1"])
    risk_agent = RiskAgent(BACKGROUND_FILES["risk_agent"]) 
    conversation_structure(risk_agent, cbt_agent, profile)

def stage_three(profile):
    cbt_agent  = CBTAgent(BACKGROUND_FILES["cbt_agent_stage3"])
    risk_agent = RiskAgent(BACKGROUND_FILES["risk_agent"])
    conversation_structure(risk_agent, cbt_agent, profile)
    
def stage_profile_management(profile, user_profile_path):
    global conversation_history
    profile_agent = ProfileAgent(BACKGROUND_FILES["profile_agent"])
    prompt = json.dumps({
        "summary_of_info"     : profile['summary_of_info'],
        "conversation_history": "\n".join(conversation_history),
        "previous_plan"       : profile['plan']                           
        })
    respond = json.loads(profile_agent.create_response(prompt))
    profile['plan']  = respond['plan']
    profile['summary_of_info'] = respond['summary_of_info']
    profile['current_session_number'] += 1
    with open(user_profile_path, "w") as user_file:
        json.dump(profile, user_file, indent=4)
    print("Save complete!")
    export_output(profile['current_session_number'], user_profile_path)

def stage_chooser(profile, user_profile_path):
    if profile['current_session_number'] <= 3:
        stage_one(profile)
    else:
        stage_three(profile)
    stage_profile_management(profile, user_profile_path)

def export_output(num, user_profile_path):
    base_name, _ = os.path.splitext(os.path.basename(user_profile_path))
    out_put_path = f'export/{base_name}_{num}.txt'
    with open(out_put_path, "w", encoding='utf-8') as file:
        for line in conversation_history:
            file.write(line + "\n") 
    conversation_history.clear()

def main():
    user_profile, user_profile_path = menu()
    stage_chooser(user_profile, user_profile_path)
    
if __name__ == "__main__":
    main()
