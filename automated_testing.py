# The `AutomatedTesting` class in the `automated_testing.py` file is a Python class that uses the
# Selenium library to automate testing of a website, including checking the title, logging in, signing
# up, and interacting with the search bar.
# automated_testing.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
# The `AutomatedTesting` class is used for automated testing of a website, where it initializes a
# Firefox driver, fetches element class names dynamically, and prints them for debugging purposes.

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
        """
        The `inspect_website` function returns the class names of the login button, signup button, and
        search bar element on a website.
        :return: The `inspect_website` function returns three variables: `login_element_class`,
        `signup_element_class`, and `search_bar_element_class`.
        """
        login_element_class = self.find_button_by_keywords(["login", "sign in"])
        signup_element_class = self.find_button_by_keywords(["sign up", "register"])
        search_bar_element_class = self.find_search_bar()

        return login_element_class, signup_element_class, search_bar_element_class
    
    def find_button_by_keywords(self, keywords):
        """
        The function finds a button on a webpage by searching for keywords in the button's text.
        
        :param keywords: The `keywords` parameter is a list of strings that represent the keywords you want
        to search for in the button text
        :return: The method `find_button_by_keywords` returns the class attribute of the first button
        element that contains any of the keywords in its text. If no button matches the keywords, it returns
        `None`.
        """
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            button_text = button.text.lower()
            for keyword in keywords:
                if keyword in button_text:
                    return button.get_attribute("class")
        return None
    def find_elements_by_attributes(self, tag, attributes, return_id=False):
        query = self.construct_attribute_xpath(attributes)
        xpath_query = f'//{tag}[{query}]'

        elements = self.driver.find_elements(By.XPATH, xpath_query)

        if return_id and elements:
            return elements[0].get_attribute("id")
        else:
            return elements
    def construct_attribute_xpath(self, attributes):
        """
        The function constructs an XPath expression based on a dictionary of attributes.
        
        :param attributes: A dictionary containing attribute names as keys and attribute values as
        values
        :return: a string that represents an XPath expression.
        """
        xpath_conditions = [f"@{key}='{value}'" for key, value in attributes.items()]
        return " and ".join(xpath_conditions)

    def get_element_class(self, element_id_or_class):
        """
        The function `get_element_class` takes an element ID or class as input and returns the class
        attribute of the element if it exists, otherwise it returns None.
        
        :param element_id_or_class: The parameter "element_id_or_class" is a string that represents
        either the ID or the class name of an HTML element
        :return: The code is returning the class attribute of the element found by the given element ID
        or class name. If the element is not found, it returns None.
        """
        try:
            element = self.driver.find_element(By.ID, element_id_or_class)
        except NoSuchElementException:
            try:
                element = self.driver.find_element(By.CLASS_NAME, element_id_or_class)
            except NoSuchElementException:
                return None

            return element.get_attribute("class")

    def test_check_title(self, expected_title):
        """
        The function checks if the actual title of a web page matches the expected title and returns a
        message indicating whether the check passed or failed.
        
        :param expected_title: The expected title is the title that you are expecting to see on the webpage.
        It is the title that you pass as an argument to the `test_check_title` function
        :return: a string that indicates whether the title check passed or failed. If the actual title
        matches the expected title, it returns "Title Check Passed" along with the actual title. If the
        actual title does not match the expected title, it returns "Title Check Failed" along with the
        expected title and the actual title.
        """
        WebDriverWait(self.driver, 60).until(EC.title_contains(expected_title))
        actual_title = self.driver.title

        # Check if the actual title matches the expected title
        if actual_title == expected_title:
            return f"Title Check Passed: {actual_title}"
        else:
            return f"Title Check Failed. Expected: {expected_title}, Actual: {actual_title}"


    def test_login(self):
        """
        The function `test_login` checks if a login element is present on a website, clicks on it, and
        returns a pass or fail message.
        :return: a string message indicating the result of the login test. If the login element class is
        not found, it returns "Login Test Skipped: Element class not found". If the login element is
        found and clicked successfully, it returns "Login Test Passed". If the login element is found but
        cannot be clicked due to being intercepted by another element, it returns "Login Test Failed:
        Element
        """
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
        """
        The function `test_sign_up` checks if a sign-up element is present on a webpage, scrolls to it,
        and clicks on it if found.
        :return: a string indicating the result of the sign-up test. The possible return values are:
        """
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
        # Specific attributes for YouTube search bar
        youtube_attributes = {"id": "search", "name": "search_query"}

        search_bar_id = self.find_elements_by_attributes("input", youtube_attributes, return_id=True)

        return search_bar_id if search_bar_id else None
    def test_search_bar(self, search_query=None):
        search_bar_attributes = {"type": "text"}

        search_bar_id = self.find_elements_by_attributes("input", search_bar_attributes, return_id=True)

        if not search_bar_id:
            return "Search Bar Test Skipped: Element ID not found"

        try:
            # Wait for the search bar to be visible and clickable
            search_bar_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, search_bar_id))
            )

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, search_bar_id))
            )

            # Perform typing into the search bar if a search query is provided
            if search_query:
                search_bar_element.clear()  # Clear any existing text
                search_bar_element.send_keys(search_query)
                search_bar_element.send_keys(Keys.RETURN)  # Press Enter after typing

                # Wait for the search results to appear (adjust the timeout as needed)
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-asin]'))
                )

            return f"Performed search using ID: {search_bar_id} with query: {search_query}"

        except Exception as e:
            print(f"Failed to interact with the search bar: {e}")
            return f"Search Bar Test Failed: {str(e)}"
            
    # def tearDown(self):
    #     """
    #     The `tearDown` function is used to close the web driver if it is open.
    #     """
    #     if self.driver:
    #         self.driver.quit()