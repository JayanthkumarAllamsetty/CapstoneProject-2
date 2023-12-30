from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
class AutomatedTesting:
    def __init__(self, url):
        # Initialize the Firefox driver
        self.driver = webdriver.Firefox()
        self.driver.get(url)

    # def find_element(self, by, value, timeout=10):
    #     try:
    #         element = WebDriverWait(self.driver, timeout).until(
    #             EC.presence_of_element_located((by, value))
    #         )
    #         return element
    #     except TimeoutException:
    #         print(f"Timed out waiting for element with {by}: {value}")

    #     try:
    #         element = self.driver.find_element(by, value)
    #         return element
    #     except NoSuchElementException:
    #         print(f"Element with {by}: {value} not found")
        
    #     return None
    # def click_element(self, by, value, timeout=10):
    #     element = self.find_element(by, value, timeout)
    #     if element:
    #         try:
    #             element.click()
    #             return True
    #         except ElementClickInterceptedException:
    #             print(f"Element with {by}: {value} is not clickable")
    #     return False

    def test_check_title(self, expected_title):
        WebDriverWait(self.driver, 60).until(EC.title_contains(expected_title))
        actual_title = self.driver.title

        if actual_title == expected_title:
            return f"Title Check Passed: {actual_title}"
        else:
            return f"Title Check Failed. Expected: {expected_title}, Actual: {actual_title}"

    def find_element(self, by, value, timeout=10):
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
        element = self.find_element(by, value, timeout)
        if element:
            try:
                element.click()
                return True
            except ElementClickInterceptedException:
                print(f"Element with {by}: {value} is not clickable")
        return False
    def is_element_clickable(self, element):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element.get_attribute("id")))
            )
            return True
        except TimeoutException:
            return False
    def test_login(self):
        login_keywords = ["login", "signin"]
        for keyword in login_keywords:
            element = self.find_element(By.XPATH, f"//*[contains(@id, '{keyword}') or contains(@class, '{keyword}')]")
            if element:
                element.click()
                time.sleep(20)
                return "Login Test Passed"
        return "Login Test Skipped: Element not found"

    def test_sign_up(self):
        signup_keywords = ["signup", "register"]
        for keyword in signup_keywords:
            element = self.find_element(By.ID, keyword) or self.find_element(By.XPATH, f"//*[contains(@class, '{keyword}')]")
            if element:
                element.click()
                time.sleep(20)
                return "Sign Up Test Passed"
        return "Sign Up Test Skipped: Element not found"
    def find_search_bar(self):
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