import os
import json
import requests
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

# Allow insecure transport for local development (YouTube/Google requirement)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# Configuration
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TWITCH_REDIRECT_URI = os.getenv('TWITCH_REDIRECT_URI')

YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
YOUTUBE_REDIRECT_URI = os.getenv('YOUTUBE_REDIRECT_URI')

# OAuth Scopes
TWITCH_SCOPES = 'channel:read:stream_key'
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_redirect_uri(platform):
    """Dynamically determine the redirect URI based on the current request host."""
    # If the URI in .env is already configured (not default), use it
    configured_uri = TWITCH_REDIRECT_URI if platform == 'twitch' else YOUTUBE_REDIRECT_URI
    if configured_uri and not configured_uri.startswith('your_') and 'localhost' not in configured_uri:
        return configured_uri

    # Otherwise, build it from the current request's host (handles ngrok automatically)
    base_url = request.host_url.rstrip('/')
    path = f"/callback/{platform}"
    return f"{base_url}{path}"

def check_credentials(platform):
    """Checks if the credentials in .env are actual keys and not placeholders."""
    if platform == 'twitch':
        return TWITCH_CLIENT_ID and not TWITCH_CLIENT_ID.startswith('your_')
    if platform == 'youtube':
        return YOUTUBE_CLIENT_ID and not YOUTUBE_CLIENT_ID.startswith('your_')
    return False

@app.route('/')
def index():
    error = request.args.get('error')
    message = request.args.get('message')
    
    # Get the current base URL (handles ngrok automatically)
    current_url = request.host_url.rstrip('/')
    is_public = 'ngrok' in current_url or 'localhost' not in current_url
    
    return render_template('index.html',
                           twitch_logged_in='twitch_token' in session,
                           youtube_logged_in='youtube_token' in session,
                           twitch_key=session.get('twitch_key'),
                           youtube_key=session.get('youtube_key'),
                           error=error,
                           message=message,
                           twitch_redirect=get_redirect_uri('twitch'),
                           youtube_redirect=get_redirect_uri('youtube'),
                           current_url=current_url,
                           is_public=is_public)

@app.route('/overlay')
def overlay():
    return render_template('overlay.html')

@app.route('/api/status')
def status():
    # Mock data for now
    return jsonify({
        'twitch': 'Streaming' if session.get('twitch_key') else 'Disconnected',
        'youtube': 'Streaming' if session.get('youtube_key') else 'Disconnected'
    })

@app.route('/export')
def export_profile():
    profile = {
        'twitch': {
            'key': session.get('twitch_key'),
            'connected': 'twitch_token' in session
        },
        'youtube': {
            'key': session.get('youtube_key'),
            'connected': 'youtube_token' in session
        },
        'overlay_url': f"http://localhost:{os.getenv('PORT', 5000)}/overlay"
    }
    
    filename = "stream_profile.json"
    try:
        with open(filename, 'w') as f:
            json.dump(profile, f, indent=4)
        return jsonify({"status": "success", "message": f"Profile saved to {filename}", "profile": profile})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Twitch OAuth ---
@app.route('/login/twitch')
def login_twitch():
    if not check_credentials('twitch'):
        return redirect(url_for('index', error="Twitch Client ID is missing or invalid in your .env file."))
    
    redirect_uri = get_redirect_uri('twitch')
    params = {
        'client_id': TWITCH_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': TWITCH_SCOPES
    }
    auth_url = f"https://id.twitch.tv/oauth2/authorize?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback/twitch')
def callback_twitch():
    code = request.args.get('code')
    error_desc = request.args.get('error_description')
    
    if error_desc:
        return redirect(url_for('index', error=f"Twitch Error: {error_desc}"))
    if not code:
        return redirect(url_for('index', error="Twitch login failed: No code received"))

    try:
        redirect_uri = get_redirect_uri('twitch')
        # Exchange code for token
        token_url = "https://id.twitch.tv/oauth2/token"
        data = {
            'client_id': TWITCH_CLIENT_ID,
            'client_secret': TWITCH_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        response = requests.post(token_url, data=data)
        token_data = response.json()
        
        if response.status_code != 200:
            return redirect(url_for('index', error=f"Twitch Token Error ({response.status_code}): {token_data.get('message', 'Invalid request. Ensure the Redirect URI in Twitch Console matches the one below.')}"))

        session['twitch_token'] = token_data.get('access_token')

        # Fetch Stream Key
        headers = {
            'Client-ID': TWITCH_CLIENT_ID,
            'Authorization': f"Bearer {session['twitch_token']}"
        }
        user_response = requests.get("https://api.twitch.tv/helix/users", headers=headers)
        user_data = user_response.json()
        
        if 'data' in user_data and len(user_data['data']) > 0:
            user_id = user_data['data'][0]['id']
            session['twitch_key'] = f"live_{user_id}_xxxxxx" 
        
        return redirect(url_for('index'))
    except Exception as e:
        return redirect(url_for('index', error=f"Twitch callback error: {str(e)}"))

# --- YouTube OAuth ---
@app.route('/login/youtube')
def login_youtube():
    if not check_credentials('youtube'):
        return redirect(url_for('index', error="YouTube Client ID is missing or invalid in your .env file."))

    try:
        redirect_uri = get_redirect_uri('youtube')
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": YOUTUBE_CLIENT_ID,
                    "client_secret": YOUTUBE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=YOUTUBE_SCOPES
        )
        flow.redirect_uri = redirect_uri
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        session['youtube_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        return redirect(url_for('index', error=f"YouTube login error: {str(e)}"))

@app.route('/callback/youtube')
def callback_youtube():
    error = request.args.get('error')
    if error:
        return redirect(url_for('index', error=f"YouTube Error: {error}"))

    try:
        redirect_uri = get_redirect_uri('youtube')
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": YOUTUBE_CLIENT_ID,
                    "client_secret": YOUTUBE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=YOUTUBE_SCOPES,
            state=session.get('youtube_state')
        )
        flow.redirect_uri = redirect_uri
        
        # Explicitly fetch token using the same redirect URI
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        session['youtube_token'] = credentials.to_json()

        youtube = build('youtube', 'v3', credentials=credentials)
        request_streams = youtube.liveStreams().list(part="cdn", mine=True)
        response = request_streams.execute()
        
        if 'items' in response and len(response['items']) > 0:
            stream_key = response['items'][0]['cdn']['ingestionInfo']['streamName']
            session['youtube_key'] = stream_key

        return redirect(url_for('index'))
    except Exception as e:
        return redirect(url_for('index', error=f"YouTube callback error: {str(e)}"))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
