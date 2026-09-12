import re

USER_INPUT = """
Hello, my name is aryan and my email is Aryan@networknuts.Net
Please draft an email to my employer at InfO@networknuts.NET for
requesting 10 days of PTO.
"""

normalized_input = USER_INPUT.lower()

result = re.findall(r"[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+",normalized_input)
refined_result = re.findall(r"\w+@\w+\.\w+",normalized_input)

sanitized_input = re.sub(r"\w+@\w+\.\w+","<REDACTED_EMAIL>",normalized_input)
print(sanitized_input)