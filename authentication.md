# Guide to Authenticate and Obtain Google Slides API Key on Google Cloud Console

## Step 1: Sign in to Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with your Google account.

## Step 2: Create a New Project
1. In the top left corner, click on the **Project** icon.
2. Click on **New Project**.
3. Name your project and select the billing account if necessary.
4. Click **Create**.

## Step 3: Enable API
1. Once the project is created, in the dashboard, click on **API & Services**.
2. Select **Library**.
3. In the search bar, type **Google Slides API** and **Generative AI API**.
4. Select **Google Slides API** and **Generative AI API** from the search results.
5. Click **Enable**.
6. Wait until they are all active

## Step 4: Create API Key
1. Go back to **API & Services** from the dashboard.
2. Select **Credentials** (the key icon).
3. Click on **Create Credentials**.
4. From the dropdown menu, select **API key**.
5. Google Cloud will generate a new API key. Copy this API key to use in your application.

## Step 5: Configure the API Key
1. After the API key is created, you can configure it by clicking on the API key in the credentials list.
2. You can set restrictions for the API key, such as:
   - **Application restrictions**: Restrict the key to be used only for specific application types like websites, Android, or iOS apps.
   - **API restrictions**: Restrict the key to call only certain APIs (Select **Google Slides API**).
3. Once configured, click **Save**.

## Step 6: Create and Download OAuth 2.0 Credentials JSON File
1. On the **Credentials** page, click on **Create Credentials** and select **OAuth Client ID**.

2. If this is your first time creating an OAuth Client ID, you need to configure the **OAuth Consent Screen**:
   - Choose the user type (External or Internal).
   - Fill in the required information, including the app name, support email, and privacy policy URL (if applicable).
   - Click **Save and Continue** when finished.

3. Once configured, go back to **Create OAuth 2.0 Client ID**:
   - Select the appropriate **Application type** (Web application, Desktop app, Android, iOS, etc.). For testing a slide translation program, choose the desktop app.
   - Name the OAuth Client ID.

4. Click **Create**.

5. After the OAuth Client ID is created, you will see an option to download the JSON file. Click **Download** to save the JSON file to your computer.
   - This JSON file contains necessary information like `client_id`, `client_secret`, and authentication URLs to be used in your application.
   - rename the json file as `credentials.json`

## Step 7: Use the API Key and JSON File in Your Application
1. **API Key**: Insert the API key into your code when making requests to the Google Slides API.
2. **JSON File**: The JSON file will be used to authenticate OAuth 2.0 when your application requests access to a user's Google account. You need to configure the appropriate Google Client SDK or library to use this file.