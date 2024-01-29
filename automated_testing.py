# The above class is a Python script that uses the Selenium library to automate testing of web pages,
# including checking the page title, logging in, signing up, and interacting with a search bar.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
class AutomatedTesting:
    
    def __init__(self, url):
        # Initialize the Firefox driver
        self.website_url = url
        self.driver = webdriver.Firefox()
        self.driver.get(url)


    def test_check_title(self, expected_title):
        """
        The function checks if the actual title of a web page matches the expected title and returns a
        message indicating whether the check passed or failed.
        
        :param expected_title: The expected title of the web page that you are testing
        :return: a string that indicates whether the title check passed or failed. If the actual title
        matches the expected title, it returns a string stating "Title Check Passed" along with the actual
        title. If the actual title does not match the expected title, it returns a string stating "Title
        Check Failed" along with the expected and actual titles.
        """
        WebDriverWait(self.driver, 60).until(EC.title_contains(expected_title))
        actual_title = self.driver.title

        if actual_title == expected_title:
            return f"Title Check Passed: {actual_title}"
        else:
            return f"Title Check Failed. Expected: {expected_title}, Actual: {actual_title}"

    def find_element(self, by, value, timeout=10):
        """
        The function `find_element` is used to locate and return an element on a web page using different
        strategies, such as waiting for the element to be present or directly finding it.
        
        :param by: The "by" parameter specifies the method used to locate the element. It can take values
        such as "id", "name", "class name", "tag name", "link text", "partial link text", "css selector",
        or "xpath"
        :param value: The "value" parameter represents the value used to locate the element. It can be a
        string representing the ID, name, class name, CSS selector, XPath, or other attributes of the
        element. The specific value depends on the "by" parameter, which determines the method used to
        locate the element
        :param timeout: The `timeout` parameter is the maximum amount of time (in seconds) that the code
        will wait for the element to be located before timing out and throwing a `TimeoutException`. The
        default value is 10 seconds, but you can override it by passing a different value when calling the
        `find_element, defaults to 10 (optional)
        :return: the element if it is found, or None if the element is not found.
        """
        try:
            print(f"Trying to find element with {by}: {value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"Found element with {by}: {value}")
            return element
        except TimeoutException:
            print(f"Timed out waiting for element with {by}: {value}")

        try:
            element = self.driver.find_element(by, value)
            print(f"Found element with {by}: {value}")
            return element
        except NoSuchElementException:
            print(f"Element with {by}: {value} not found")

        return None
    def click_element(self, by, value, timeout=10):
        """
        The function `click_element` finds an element on a web page using a specified locator strategy and
        value, and then attempts to click on it, returning True if successful and False otherwise.
        
        :param by: The "by" parameter specifies the method used to locate the element. It can take values
        such as "id", "name", "class name", "xpath", "css selector", etc. This parameter is used in the
        "find_element" method to locate the element
        :param value: The "value" parameter in the "click_element" method represents the value of the
        attribute that is used to locate the element on the web page. It could be the id, name, class,
        xpath, etc. depending on the "by" parameter
        :param timeout: The timeout parameter is the maximum amount of time (in seconds) that the code will
        wait for the element to be found before raising an exception. If the element is not found within the
        specified timeout, a NoSuchElementException will be raised, defaults to 10 (optional)
        :return: a boolean value. It returns True if the element is found and successfully clicked, and
        False if the element is not found or is not clickable.
        """
        element = self.find_element(by, value, timeout)
        if element:
            try:
                element.click()
                return True
            except ElementClickInterceptedException:
                print(f"Element with {by}: {value} is not clickable")
        return False
    def is_element_clickable(self, element):
        """
        The function checks if an element is clickable within a specified time limit.
        
        :param element: The "element" parameter is the web element that you want to check if it is clickable
        or not
        :return: a boolean value. If the element is clickable within the specified timeout period, it will
        return True. Otherwise, if the element is not clickable within the timeout period, it will return
        False.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element.get_attribute("id")))
            )
            return True
        except TimeoutException:
            return False
    def test_login(self, email, password):
        try:
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'login_click')]"))
            )
            login_button.click()

            # Wait for the login container to appear
            login_container_class = "modal-header"
            login_container = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, login_container_class))
            )

            assert login_container.is_displayed(), "Login container is displayed after clicking Log In"

            # Now enter the email and password
            email_input = self.driver.find_element(By.ID, "si_popup_email")
            password_input = self.driver.find_element(By.ID, "si_popup_passwd")

            email_input.send_keys(email)
            password_input.send_keys(password)

            # Click the login button using JavaScript
            login_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'clik_btn_log btn-block')]")
            self.driver.execute_script("arguments[0].click();", login_button)
            sleep(20)
            return "Login Test Passed"
        except TimeoutException:
            return "Login button did not become clickable within 20 seconds."
        except Exception as e:
            return f"Login Test Failed: {str(e)}"

    def test_sign_up(self, email, mobile_number):
        try:
            # Find the sign-up element
            signup_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'signup')]"))
            )
            signup_element.click()

            # Find the email input
            email_input = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "sg_popup_email"))
            )
            email_input.send_keys(email)

            # Find the mobile number input
            mobile_input = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "sg_popup_phone_no"))
            )
            mobile_input.send_keys(mobile_number)

            # Scroll elements into view
            self.driver.execute_script("arguments[0].scrollIntoView();", email_input)
            self.driver.execute_script("arguments[0].scrollIntoView();", mobile_input)

            # Perform additional actions if needed

            # Click the sign-up button
            signup_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign Up')]")
            signup_button.click()

            return "Sign Up Test Passed"

        except Exception as e:
            return f"Sign Up Test Failed: {str(e)}"
    def find_search_bar(self):
        """
        The function `find_search_bar` searches for a search bar element on a web page and returns the first
        matching element.
        :return: the search bar element if it is found, or None if it is not found or if there is an error.
        """
        try:
            # Find input elements with the word 'search' in attributes
            search_bar_elements = self.driver.find_elements(By.XPATH, "//input[contains(@id, 'search') or contains(@class, 'search')]")

            if search_bar_elements:
                # Pick the first matching element (you may adjust this based on your HTML structure)
                search_bar_element = search_bar_elements[0]
                print(f"Found search bar element: {search_bar_element}")
                return search_bar_element

            print("Search bar element not found.")
            return None
        except Exception as e:
            print(f"Error finding search bar element: {e}")
            return None
    def test_search_bar(self, search_query=None):
        """
        The function tests the search bar by entering a search query and returning a message indicating
        the success or failure of the test.
        
        :param search_query: The search_query parameter is a string that represents the query to be
        entered into the search bar. It is an optional parameter, so if no value is provided, the search
        bar will not be interacted with and the function will return a message indicating that the test
        was skipped
        :return: a string indicating the result of the search bar test. If the search bar element is not
        found, it returns "Search Bar Test Skipped: Element not found". If there is an exception while
        interacting with the search bar, it returns "Search Bar Test Failed" followed by the error
        message. Otherwise, it returns "Performed search using CSS Selector: input[type='search'] with
        query
        """
        search_bar_element = self.find_search_bar()

        if not search_bar_element:
            return "Search Bar Test Skipped: Element not found"

        try:
            if search_query:
                search_bar_element.send_keys(search_query)
                search_bar_element.send_keys(Keys.RETURN)
            return f"Performed search using CSS Selector: input[type='search'] with query: {search_query}"
        except Exception as e:
            print(f"Failed to interact with the search bar: {e}")
            return f"Search Bar Test Failed: {str(e)}"

    def tearDown(self):
        if self.driver:
            self.driver.quit()