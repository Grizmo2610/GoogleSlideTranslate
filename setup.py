import os
import json


def setUpModel(path):
    os.system('cls')
    os.system('pip install -r requirements.txt')
    os.system('cls')
    with open(path, 'r') as f:
        data = json.load(f)

    os.environ['GEMINI_API_KEY'] = data['GeminiKey']