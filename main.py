# main.py
from ai_model import interpret_and_execute

website_url = "https://www.amazon.in"
command = "Run tests on search bar"
results = interpret_and_execute(website_url, command)
print("Results:", results)
