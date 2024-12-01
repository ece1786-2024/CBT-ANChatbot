import os
import json
import uuid

def register():
    # Ensure the 'users' directory exists
    if not os.path.exists("users"):
        os.makedirs("users")

    # Get user information
    name = input("Enter your name: ")
    height = input("Enter your height (e.g., 5'5''): ")
    weight = input("Enter your weight (e.g., 115 lbs): ")

    # Generate a unique user ID
    user_id = str(uuid.uuid4())

    # Create the user data
    user_data = {
        "current_session_number": 0,
        "name_of_patient": name,
        "summary_of_info": f"{name} is {height} and weighs {weight}.",
        "plan": {
            "cognitive_restructuring_plan": "",
            "behavioral_intervention_plan": {
                "weekly_meal_plan": "",
                "exposure_therapy": "",
                "body_image_restructuring": "",
                "behavioral_monitoring": ""
            }
        }
    }

    # Save user data to a file named with the unique user ID
    user_file_path = os.path.join("users", f"{user_id}.json")
    with open(user_file_path, "w") as user_file:
        json.dump(user_data, user_file, indent=4)

    print(f"User registered successfully with ID: {user_id}")

def login():
    # Prompt user for their unique ID
    user_id = input("Enter your user ID: ")
    user_file_path = os.path.join("users", f"{user_id}.json")

    # Check if the user file exists
    if os.path.exists(user_file_path):
        with open(user_file_path, "r") as user_file:
            user_data = json.load(user_file)
            print(f"Welcome back, {user_data['name_of_patient']}!")
            return True, user_data, user_file_path
    else:
        print("User not found. Please check your ID or register first.")
        return False, None, None

def menu():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            status, userprofile, userprofilepath = login()
            if status:
                print("Lets starting the treatment")
                return userprofile, userprofilepath
            else:
                print("Login Failed! Please try again")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

