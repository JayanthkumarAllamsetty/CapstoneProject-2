# ai_model.py
from automated_testing import AutomatedTesting

def interpret_and_execute(website_url, command):
    # Import the interpret_command function from interpret_model
    from interpret_model import interpret_command

    print(f"Interpreting command: {command}")

    if interpret_command(command, "login button"):
        print(f"Initiating login testing for {website_url}")

        tester = AutomatedTesting(website_url)  # Pass the URL when creating an instance
        result = tester.test_login()
        tester.tearDown()

        print("Login testing complete. Result will be returned to the user.")
        return {"login_result": result}
    
    elif interpret_command(command, "check title"):
        print(f"Initiating title checking for {website_url}")

        tester = AutomatedTesting(website_url)
        result = tester.test_check_title("Instructor-Led Online Training with 24X7 Lifetime Support | Edureka")
        tester.tearDown()

        print("Title checking complete. Result will be returned to the user.")
        return {"title_check_result": result}
    elif interpret_command(command, "sign up"):
        print(f"Initiating sign up testing for {website_url}")

        tester = AutomatedTesting(website_url)
        result = tester.test_sign_up()
        tester.tearDown()

        print("Sign Up testing complete. Result will be returned to the user.")
        return {"sign_up_result": result}
    # Add more conditions for other types of tests if needed
    elif interpret_command(command, "search bar"):
        print(f"Initiating search bar testing for {website_url}")

        # You can replace 'your_search_query_here' with the actual search query you want to test
        search_query = 'Iphone 12'

        tester = AutomatedTesting(website_url)
        result = tester.test_search_bar(search_query)
        tester.tearDown()

        print("Search bar testing complete. Result will be returned to the user.")
        return {"search_bar_result": result}



    else:
        print("Invalid command.")
        return {"error": "Invalid command."}