from guardrails_ai.detect_pii import DetectPII
from guardrails import Guard

guard = Guard().use(
    DetectPII(pii_entities=["EMAIL_ADDRESS","PHONE_NUMBER"],on_fail=fix)
)

USER_INPUT = """
Hello, my name is aryan and my email is Aryan@networknuts.Net
Please draft an email to my employer at InfO@networknuts.NET for
requesting 10 days of PTO.
"""