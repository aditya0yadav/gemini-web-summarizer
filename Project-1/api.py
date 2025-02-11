import requests
import json
from config import URL
from bs4 import BeautifulSoup
import re

STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
    'will', 'with', 'the', 'this', 'but', 'they', 'have', 'had', 'what', 'when',
    'where', 'who', 'which', 'why', 'can', 'could', 'should', 'would', 'may',
    'might', 'must', 'shall', 'into', 'if', 'then', 'else', 'than', 'so', 'no',
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'
}

def clean_data(text):
    text = text.lower()
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    cleaned_words = [word for word in words if word not in STOPWORDS]
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text

def generate_content(prompt, context=''):
    headers = {"Content-Type": "application/json"}
    full_prompt = f"Context: {context}\n\nPrompt: {prompt}" if context else prompt
    data = {"contents": [{"parts": [{"text": full_prompt}]}]}
    
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Error: Unexpected response format"
    else:
        return f"Error: {response.status_code}, {response.text}"

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error: {str(e)}"