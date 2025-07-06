# YouTube Assistant

This is a Streamlit application that allows you to ask questions about a YouTube video and get answers based on the video's transcript.

## Usage

To run this application, you need to have Python installed on your system.

### 1. Clone the repository

```bash
https://github.com/anandraja-dev/youtube_assistant.git
cd youtube-assistant
```

### 2. Create a virtual environment and activate it

**On macOS and Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a file named `.env` in the root of the project directory and add your Google API key to it:

```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```

### 5. Run the application

```bash
streamlit run main.py
```

The application will open in your web browser. Paste a YouTube video URL, ask a question, and click "Submit" to get an answer.
