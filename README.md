# Xbox, Lightstream & Stream Sponsor Finder

A Python tool designed for Xbox players using Lightstream to find instant sponsorship opportunities and display them live on Twitch or YouTube.

## 🚀 Features

- **Lightstream Integration**: Generate a public URL using ngrok to display your overlay on Xbox streams without a PC/Capture Card.
- **Live Stream Overlay**: Professional CSS overlay that shows rotating high-value Xbox deals.
- **Instant Gaming Deals**: Fetches the latest Xbox game deals from Instant Gaming (via CheapShark API).
- **Public Bounties**: Aggregates open quests and bounties (Microsoft Rewards, Buff, etc.).

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/xbox-sponsor-finder.git
   cd xbox-sponsor-finder
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

Run the main script:

```bash
python xbox_sponsor_finder.py
```

### 📺 Using with Lightstream (Xbox One/Series)
1. Get a free ngrok token at [ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken).
2. Run the script and select **Option 4**.
3. Paste your ngrok token when prompted.
4. Copy the **LIGHTSTREAM PUBLIC URL** provided by the script.
5. In **Lightstream Studio**, add a new **Layer** -> **3rd Party** -> **Browser Source**.
6. Paste the Public URL and set dimensions to **400x600**.
7. Your Xbox stream will now show live deals and sponsorships!

## 📋 Requirements

- Python 3.7+
- `requests`, `colorama`, `flask`, `flask-cors`, `pyngrok`

## ⚖️ Disclaimer

This tool aggregates publicly available information. While it finds opportunities that don't require sign-up to *view*, actually receiving payments or claiming rewards will eventually require you to provide a payment method (like PayPal) or create an account on the respective platform's fulfillment page.

---
*Created for Xbox Gamers.*
