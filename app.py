# Google libraries
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import google.generativeai as genai

# System libraries
import os
import pickle
import time
from rich.console import Console
from rich.markdown import Markdown

import setup
from Model import SlideTranslate, GeminiModel

def get_presentation_id(url: str):
    url = url.replace('\'', '').replace('"', '').strip()
    if not url.startswith('https://docs.google.com/presentation/d/'):
        raise ValueError('Invalid presentation URL')
    return url.split('/')[5]

console = Console()

model = SlideTranslate(100)

console.print(Markdown('# Enter your Google Slides presentation URL. We only handle presentations saved in Google Slides format.'))
url = input('> ')
presentation_id = get_presentation_id(url)

console.print(Markdown('# Which language you want to translate to?'))
target_language = input('> ')

model.translated_slide(presentation_id, target_language=target_language)
console.print(Markdown('# Finished! Your slide have been translated!'))