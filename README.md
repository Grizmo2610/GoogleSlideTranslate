Here is the translation:

# Automatically Translate Google Slides Presentation

## Installation Guide

### Authenticate Account, Authorize, and Fill in Google API Key

> For details, see the file `authentication.md`.

* **Step 1:** Go to [Google Cloud Console](https://console.cloud.google.com/) and log in to your account.
* **Step 2:** Create a new project.
* **Step 3:** Navigate to: [Google Library](https://console.cloud.google.com/apis/library) and enable the required services.
* **Step 4:** Create OAuth 2.0 Client ID credentials and then download the JSON file.
* **Step 5:** Create a new API key.
* **Step 6:** Create a `key.json` file with the following structure:

```json
{
    "GeminiKey": "YOUR GOOGLE API KEY"
}
```

### Setting Up Paths

There are two important files: the `key.json` file containing the API key and the `credentials.json` file containing authentication information. Change the paths to these files in `Model.py` at lines 25 and 26.

Additionally, a file named `token.pickle` will be generated after authentication. Set the path (where you want to save this file) at line 27 in the `Model.py` file.

## Usage Guide

In the `app.py` file, set the maximum number of requests. Note, the heavier the slide (more pages, more content), the lower the limit should be (less than 10 is best).

At first time run, you will need 

Run the `app.py` file and wait for the necessary libraries to install. Once completed, enter the link to your Google Slides presentation and paste it. Then, select the language you want to translate into. You can write in any format/language (e.g., vie, vietnamese, vietnam, Việt Nam, Tiếng Việt, etc.), all will be accepted.

**Note:** If you want to translate a slide that is not yours, ensure that the slide allows your authenticated Gmail account (authenticated with Google) to edit the presentation. Otherwise, the program will return an error.