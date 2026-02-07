# Stream Overlay Generator (Encrypted)

This Python program generates dynamic stream overlays for Twitch and YouTube. The overlay configuration (username, sponsor, colors, etc.) is encrypted using the stream key, ensuring that the overlay data is tied to the streamer's unique key.

## Features

- **Encryption**: Uses AES-256 (Fernet) to encrypt overlay data.
- **Dynamic Content**: Easily change username, platform, and sponsor.
- **OBS Ready**: Generates a URL that can be added directly to OBS as a Browser Source.
- **Customizable**: simple HTML/CSS template for easy styling.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sponsor-for-stream.git
   cd sponsor-for-stream
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the Overlay Server

The server handles the decryption and rendering of the overlay.

```bash
python app.py
```

By default, it runs on `http://localhost:5000`.

### 2. Generate an Overlay URL

Use the `generator.py` script to create your unique, encrypted overlay URL.

```bash
python generator.py --key YOUR_STREAM_KEY --username "MyStreamerName" --platform "Twitch" --sponsor "CoolSponsor" --color "#00ff00"
```

Replace `YOUR_STREAM_KEY` with your actual Twitch or YouTube stream key (or any secret string).

### 3. Add to OBS

1. Copy the generated `Overlay URL`.
2. In OBS, add a new **Browser Source**.
3. Paste the URL into the **URL** field.
4. Set the width and height (e.g., 1920x1080) and check "Shutdown source when not visible".

## Project Structure

- `app.py`: The Flask web server.
- `utils.py`: Encryption and decryption logic.
- `generator.py`: CLI tool for generating encrypted URLs.
- `templates/`: HTML templates for the overlays.
- `static/`: Placeholder for CSS/JS files.

## Security Note

This tool uses your stream key as an encryption key. While this ties the overlay to your stream, **be careful not to share the generated URL publicly**, as it contains your stream key in the query parameters. In a production environment, you should use a backend database to map encrypted IDs to stream keys instead of passing the key in the URL.

## License

MIT
