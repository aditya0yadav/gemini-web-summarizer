import os
# print()

GEMINI_API_KEY = os.getenv("gemini")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
