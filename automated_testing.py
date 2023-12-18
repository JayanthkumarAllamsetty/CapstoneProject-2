# automated_testing.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException

class AutomatedTesting:
    def __init__(self, url):
        # Initialize the Firefox driver
        self.driver = webdriver.Firefox()
        self.driver.get(url)

        # Fetch element class names dynamically
        self.login_element_class, self.signup_element_class, self.search_bar_element_class = self.inspect_website()

        # Print fetched class names for debugging
        print(f"Login Element Class: {self.login_element_class}")
        print(f"Sign Up Element Class: {self.signup_element_class}")
        print(f"Search Bar Element Class: {self.search_bar_element_class}")

    possible_login_texts = ["Log In", "Sign In", "Login", "Sign In Here"]  # Add more variations as needed

    def inspect_website(self):
        login_element_class = self.find_button_by_keywords(["login", "sign in"])
        signup_element_class = self.find_button_by_keywords(["sign up", "register"])
        search_bar_element_class = self.find_search_bar()

        return login_element_class, signup_element_class, search_bar_element_class
    
    def find_button_by_keywords(self, keywords):
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            button_text = button.text.lower()
            for keyword in keywords:
                if keyword in button_text:
                    return button.get_attribute("class")
        return None

    def find_element_by_attribute(self, tag, attributes, return_id=False):
            try:
                element = self.driver.find_element(By.TAG_NAME, tag)
                if return_id:
                    return element.get_attribute("id")
                else:
                    return element.get_attribute("class")
            except NoSuchElementException:
                return None
    def construct_attribute_xpath(self, attributes):
        xpath_conditions = [f"@{key}='{value}'" for key, value in attributes.items()]
        return " and ".join(xpath_conditions)

    def get_element_class(self, element_id_or_class):
            try:
                element = self.driver.find_element(By.ID, element_id_or_class)
            except NoSuchElementException:
                try:
                    element = self.driver.find_element(By.CLASS_NAME, element_id_or_class)
                except NoSuchElementException:
                    return None

            return element.get_attribute("class")

    def test_check_title(self, expected_title):
        WebDriverWait(self.driver, 60).until(EC.title_contains(expected_title))
        actual_title = self.driver.title

        # Check if the actual title matches the expected title
        if actual_title == expected_title:
            return f"Title Check Passed: {actual_title}"
        else:
            return f"Title Check Failed. Expected: {expected_title}, Actual: {actual_title}"


    def test_login(self):
        login_element_class = self.inspect_website()[0]

        if not login_element_class:
            return "Login Test Skipped: Element class not found"

        try:
            login_element = self.driver.find_element(By.CLASS_NAME, login_element_class)
            login_element.click()
            return "Login Test Passed"
        except ElementClickInterceptedException:
            return "Login Test Failed: Element not clickable"
    def test_sign_up(self):
        if not self.signup_element_class:
            return "Sign Up Test Skipped: Element class not found"

        # Split the class names if there are multiple classes
        signup_classes = self.signup_element_class.split()

        # Print the class names for debugging
        print(f"Signup Classes: {signup_classes}")

        # Wait for the obscuring element to be present
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "new_sign_up_optim"))
            )
        except Exception as e:
            print(f"Failed to wait for obscuring element: {e}")
            return "Sign Up Test Failed: Unable to wait for obscuring element"

        # Scroll to the sign-up element
        sign_up_element = None
        for signup_class in signup_classes:
            try:
                sign_up_element = self.driver.find_element(By.CLASS_NAME, signup_class)
                break
            except NoSuchElementException:
                pass  # Continue to the next class name

        if sign_up_element:
            self.driver.execute_script("arguments[0].scrollIntoView();", sign_up_element)
            
            try:
                sign_up_element.click()
                return "Sign Up Test Passed"
            except Exception as e:
                print(f"Failed to click sign-up element: {e}")
                return "Sign Up Test Failed: Click failed"
        else:

            return "Sign Up Test Failed: Element not found with any of the given classes"
    def find_search_bar(self):
        # Check for the search bar by attributes
        search_bar_element = self.find_element_by_attribute("input", {"type": "search"})
        return search_bar_element

        return None
    
    def test_search_bar(self, search_query=None):
        search_bar_id = self.find_element_by_attribute("input", {"type": "search"}, return_id=True)

        if not search_bar_id:
            return "Search Bar Test Skipped: Element ID not found"

        try:
            search_bar_element = self.driver.find_element(By.ID, search_bar_id)

            if search_query:
                # Use JavaScript to set the value of the input field
                self.driver.execute_script("arguments[0].value = arguments[1];", search_bar_element, search_query)

                # Submit the form (hit Enter key)
                search_bar_element.send_keys(Keys.RETURN)

            return f"Performed search using ID: {search_bar_id} with query: {search_query}"

        except Exception as e:
            print(f"Failed to interact with the search bar: {e}")
            return f"Search Bar Test Failed: {str(e)}"
    def tearDown(self):
        if self.driver:
            self.driver.quit()
