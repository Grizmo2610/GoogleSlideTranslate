import os
import json


def setUpModel(path):
    with open(path, 'r') as f:
        data = json.load(f)

    os.environ['GOOGLE_API_KEY'] = data['GeminiKey']