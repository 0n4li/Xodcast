# Xodcast

Xodcast is a web application that leverages AI to generate podcasts from user-provided topics. It uses Google's Gemini API to create a conversational script and then converts it into an audio podcast using Google's Text-to-Speech service.

## Features

*   **Topic-Based Podcast Generation:** Generates a podcast script based on a user-provided topic.
*   **Customizable Settings:** Allows users to customize the podcast generation process through various settings.
*   **Multi-Speaker Support:** Can generate podcasts with multiple speakers, assigning different voices to each speaker.
*   **Emotional Tone:** Applies emotional tones to the generated speech to make it more engaging.
*   **Audio Streaming:** Supports streaming of the generated audio as it's being created.
*   **Task Management:** Manages audio generation tasks, allowing users to check the status and retrieve the generated audio.
*   **Configurable Output Format:** Supports different audio output formats (e.g., WAV, MP3).

## Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/0n4li/Xodcast.git
    cd xodcast
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure .env File:**

    A sample `.env.example` file has been provided. Copy it using the below command:

    ```bash
    cp .env.example .env
    ```

    Update the values for `GOOGLE_API_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`, `GEMINI_MODEL`, and `FLASK_PORT` in the `.env` file.

    ```bash
    GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>
    GOOGLE_APPLICATION_CREDENTIALS=<PATH_TO_YOUR_SERVICE_ACCOUNT_KEY_FILE>
    GEMINI_MODEL=gemini-exp-1206
    FLASK_PORT=5000
    ```

## Usage

1. **Run the Application:**

    ```bash
    python app.py
    ```

    This will start the Flask development server.

2. **Access the Web Interface:**

    Open your web browser and go to `http://localhost:5000`.

3. **Generate a Podcast:**

    *   Enter a topic for the podcast.
    *   Adjust the settings as desired (optional).
    *   Click the "Generate Script" button to generate the conversation script.
    *   Click the "Generate Audio" button to convert the script into audio.
    *   You can monitor the audio generation progress and stream the audio as it's being created.
    *   Once completed, you can download the generated audio file.

## Contributing

Feel free to fork the project, create a new branch, make your changes, and create a pull request. Please adhere to standard coding practices and include tests where appropriate.
