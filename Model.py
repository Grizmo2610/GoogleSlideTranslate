# Import Google libraries for authentication and API interaction
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Import Google Gemini API libraries for generative AI tasks
import google.generativeai as genai
from google.generativeai import GenerativeModel

# Import system libraries for file handling and setup tasks
import os
import pickle
import setup
import json
import sys


sys.setrecursionlimit(100)

if not os.path.exists('./Data'):
    os.makedirs('./Data')

# Constants for configuration settings
GEMINI_DEFAULT_MODEL = 'gemini-1.5-flash'  # Default generative model for Gemini API
KEY_PATH = 'Data/Key.json'  # Path to the file containing the API key (update to the actual path)
CREDENTIALS_FILE = 'Data/credentials.json'  # Path to the JSON file with Google OAuth2 credentials
TOKEN_FILE = 'Data/token.pickle'  # Path to the file for storing authentication tokens. NO NEED TO CHANGE

# Scopes defining the permissions requested by the application
SCOPES = [
    'https://www.googleapis.com/auth/presentations',  # Permission to manage Google Slides presentations
    'google.cloud.translate.v2.TranslateService.TranslateText'  # Permission to use Google Cloud Translation API
]

def get_credentials():
    """
    Authenticate the user and return Google API credentials.

    Returns:
        Credentials: The authenticated credentials for accessing Google APIs.
    """
    creds = None
    # Check if a token file exists to load saved credentials
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)  # Load saved credentials from file

    # If no valid credentials are found, initiate a new authentication flow
    if not creds or not creds.valid:
        # If credentials are expired, refresh them
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # If no valid credentials exist, start a new authentication flow
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)  # Open a local server for user authentication
        # Save the new credentials for future use
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Build the Google Slides API service instance using the authenticated credentials
service = build('slides', 'v1', credentials=get_credentials())

class GeminiModel:
    """
    A class for interacting with the Gemini API to perform generative AI tasks.
    """
    def __init__(self, model = 'gemini-1.5-flash', key = ...) -> None:
        self.model = GenerativeModel(model)
        try:
            if key == ...:
                self.key = os.environ["GOOGLE_API_KEY"]
            else:
                self.key = key
        except:
            print(os.environ['GOOGLE_API_KEY'])
        genai.configure(api_key=self.key)
    
    def response(self, text, prompt):
        response =  self.model.generate_content(f"{prompt}\n{text}\n")
        final = ''
        for chunk in response:
            final += chunk.text + '\n'
        return final.strip()


class SlideTranslate:
    """
    A class for translating the content of Google Slides presentations using the Gemini API.
    """
    
    PROMPT = 'Translate the following text from {src_language} into {target_language}. Only translate the text, do not return any other characters. Major of text is {major}'

    def __init__(self, max_request=30) -> None:
        """
        Initialize the SlideTranslate instance with the Google Slides API service and Gemini model.

        Args:
            max_request (int): The maximum number of requests per batch.
        """
        setup.setUpModel(KEY_PATH)
        self.service = service  # Initialize with Google Slides API service
        self.gemini_model = GeminiModel()  # Initialize Gemini model for translation
        self.max_request = max_request  # Set the maximum number of requests per batch

    def valid_string(self, text: str) -> bool:
        """
        Validate if a string is suitable for translation.

        Args:
            text (str): The string to be validated.

        Returns:
            bool: True if the string is valid for translation, otherwise False.
        """
        return len(text) >= 5 and not text.startswith('https:') and text != 'Source: '

    def make_request(self, all_request: list, presentation_id: str):
        """
        Send batch requests to the Google Slides API for text replacement.

        Args:
            all_request (list): The list of requests to be sent.
            presentation_id (str): The ID of the Google Slides presentation.

        Returns:
            dict: The response from the Google Slides API.
        """
        all_response = []
        # Sort requests by text length in descending order to prioritize longer texts
        all_request.sort(key=lambda x: len(x['replaceAllText']['containsText']['text']), reverse=True)
        
        print(f'Request size: {len(all_request)}')
        # Split requests into batches if the number exceeds the maximum allowed
        if all_request:
            if len(all_request) > self.max_request:
                for i in range(0, len(all_request), self.max_request):
                    print(f'{i}/{len(all_request)}')
                    body = {'requests': all_request[i:i+self.max_request]}  # Prepare batch request body
                    all_response.append(
                        self.service.presentations().batchUpdate(
                            presentationId=presentation_id, 
                            body=body
                        ).execute()
                    )
            else:
                # If the number of requests is within the limit, send them in one batch
                body = {'requests': all_request}
                all_response = self.service.presentations().batchUpdate(
                    presentationId=presentation_id, body=body
                ).execute()
            
            return all_response  # Return the responses from the Google Slides API

    def find_text_in_group(self, elements):
        texts = []
        
        for element in elements:
            if 'shape' in element:
                text_elements = element['shape'].get('text')
                if text_elements:
                    text_elements = text_elements['textElements']
                    for text in text_elements:
                        if 'textRun' in text:
                            texts.append(text['textRun']['content'])

            elif 'elementGroup' in element:
                group_elements = element['elementGroup'].get('children')
                if group_elements:
                    texts.extend(self.find_text_in_group(group_elements))

        return texts

    def generate_body(self, translated_text: str, current_text: str) -> dict:
        """
        Generate the request body for replacing text in a slide with the translated version.

        Args:
            translated_text (str): The translated text to replace with.
            current_text (str): The original text to be replaced.

        Returns:
            dict: The body of the request for text replacement.
        """
        return {
            'replaceAllText': {
                'replaceText': translated_text,  # The text to use for replacement
                'containsText': {
                    'text': current_text,  # The text to be replaced
                    'matchCase': True  # Match case exactly
                }
            }
        }
        
    def translated_slide(self, presentation_id: str, src_language: str='English', target_language: str='Vietnamese', major: str = 'IT') -> tuple:
        """
        Translate the entire content of a Google Slides presentation.

        Args:
            presentation_id (str): The ID of the Google Slides presentation to be translated.
            src_language (str, optional): The source language of the text. Defaults to 'English'.
            target_language (str, optional): The target language for translation. Defaults to 'Vietnamese'.
            major: (str, optional): The major of the original text
        Returns:
            tuple: A tuple containing two elements:
                - A list of elements that failed translation.
                - The responses from the Google Slides API.
        """
        PROMPT_INPUT = self.PROMPT.format(src_language=src_language, target_language=target_language, major=major)
        all_request = []  # List to store all text replacement requests
        presentation = self.service.presentations().get(presentationId=presentation_id).execute()  # Get the presentation details
        slides = presentation.get('slides', [])  # Extract slides
        exception_slides = []  # List to store elements that failed translation

        # Iterate through each slide and its elements to extract and translate text
        for i in range(len(slides[:5])):
            print(f'Processing slide {i+1}/{len(slides)}')
            slide = slides[i]
            elements = slide.get('pageElements')
            all_text = self.find_text_in_group(elements)
            for current_text in all_text:
                try:
                    # Extract text from the current element
                    if isinstance(current_text, str):
                        # If the text is a string and valid for translation
                        if current_text and len(current_text) >= 5:
                            # Generate the translated text
                            translated_text = self.gemini_model.response(current_text, PROMPT_INPUT)
                            # Prepare and add the request for text replacement
                            all_request.append(self.generate_body(translated_text, current_text))
                    elif isinstance(current_text, list):
                        # If the text is a list, process each string
                        for text in current_text:
                            if len(text) >= 5:
                                translated_text = self.gemini_model.response(text, PROMPT_INPUT)
                                all_request.append(self.generate_body(translated_text, text))
                except Exception as e:
                    # If an error occurs, add the element to the exception list
                    exception_slides.append(current_text)           
        # Send all collected requests in batches and get the response
        all_response = self.make_request(all_request, presentation_id)
        return exception_slides, all_response  # Return failed elements and API responses