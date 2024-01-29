from ai_model import interpret_and_execute

website_url = "https://edureka.co/"
command = "Run tests on login button"

# Adjust based on the command
if "login" in command.lower():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    results = interpret_and_execute(website_url, command, email=email, password=password)
elif "signup" in command.lower():
    email = input("Enter your email: ")
    mobile_number = input("Enter your mobile number: ")
    results = interpret_and_execute(website_url, command, email=email, mobile_number=mobile_number)
else:
    # Handle other commands or provide an error message
    results = {"error": "Invalid command."}

print("Results:", results)