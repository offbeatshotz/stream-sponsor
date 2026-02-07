# Stream Overlay Generator & Key Manager

A Python-based tool to generate dynamic stream overlays and automatically retrieve stream keys from Twitch and YouTube.

## Features
- **OAuth Integration**: Securely connect to Twitch and YouTube.
- **Stream Key Retrieval**: Automatically fetch your current stream key/URL.
- **Overlay Generator**: Create customizable HTML/JS overlays for your stream.
- **Local Server**: Hosted locally for easy integration with OBS/Streamlabs.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API credentials.
4. Run the application:
   ```bash
   python main.py
   ```

## API Setup
### Twitch
1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console).
2. Register a new application.
3. Set the Redirect URI to `http://localhost:5000/callback/twitch` (or your ngrok URL). **IMPORTANT: This must match your `.env` file exactly.**
4. Copy the Client ID and Secret to your `.env` file.

### YouTube
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the "YouTube Data API v3".
3. Create OAuth 2.0 credentials and set the Redirect URI to `http://localhost:5000/callback/youtube` (or your ngrok URL). **IMPORTANT: This must match your `.env` file exactly.**
4. Copy the Client ID and Secret to your `.env` file.

## Usage
1. **Login**: Click "Login with Twitch" or "Login with YouTube" to authorize the app.
2. **Stream Keys**: Once authorized, your stream keys will be fetched and displayed.
3. **Overlay**: Access the overlay at `http://localhost:5000/overlay`.
4. **Export**: Click "Export Stream Profile" to save your configuration to `stream_profile.json`.

## Integrating with Lightstream
Since Lightstream is a cloud-based studio, it cannot access `localhost` directly. You must make your local server publicly accessible using a tool like **ngrok**.

### 1. Make your overlay public with ngrok
1. Download [ngrok](https://ngrok.com/).
2. Run your Python app: `python main.py`.
3. In a new terminal, run:
   ```bash
   ngrok http 5000
   ```
4. Copy the "Forwarding" URL (e.g., `https://xxxx-xxxx.ngrok-free.app`). Your overlay URL for Lightstream will be `https://xxxx-xxxx.ngrok-free.app/overlay`.

### 2. Add to Lightstream
1. Open your [Lightstream Studio](https://studio.golightstream.com/).
2. Click the **"+" (Add Layer)** button.
3. Select **"3rd Party Integration"** or **"External Asset"** -> **"Browser Source"**.
4. Paste your ngrok Overlay URL.
5. Set the resolution to match your canvas (e.g., 1280x720 or 1920x1080).

## Project Structure
- `main.py`: Flask application handling OAuth and API calls.
- `templates/`: HTML templates for the dashboard and overlay.
- `requirements.txt`: Python dependencies.
- `.env`: (You create this) Stores your API credentials.
