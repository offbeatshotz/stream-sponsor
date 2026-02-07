import json
import argparse
from utils import encrypt_data

def main():
    parser = argparse.ArgumentParser(description="Generate an encrypted overlay URL.")
    parser.add_argument("--key", required=True, help="The stream key to use for encryption.")
    parser.add_argument("--platform", default="Twitch", help="Streaming platform (Twitch/YouTube).")
    parser.add_argument("--username", required=True, help="Streamer username.")
    parser.add_argument("--sponsor", help="Sponsor name to display.")
    parser.add_argument("--color", default="#ff0000", help="Accent color (hex code).")
    parser.add_argument("--host", default="http://localhost:5000", help="The base URL where the overlay server is hosted.")

    args = parser.parse_args()

    payload = {
        "platform": args.platform,
        "username": args.username,
        "sponsor": args.sponsor,
        "color": args.color
    }

    payload_json = json.dumps(payload)
    encrypted_payload = encrypt_data(payload_json, args.key)

    overlay_url = f"{args.host}/overlay?data={encrypted_payload}&key={args.key}"

    print("\n--- Overlay Generation Successful ---")
    print(f"Platform: {args.platform}")
    print(f"Username: {args.username}")
    print(f"Sponsor:  {args.sponsor if args.sponsor else 'None'}")
    print("-" * 37)
    print(f"Your Overlay URL (Add this to OBS Browser Source):")
    print(overlay_url)
    print("-" * 37)

if __name__ == "__main__":
    main()
