# Xbox, Lightstream & XPN Sponsor Finder

A Python tool designed for Xbox players using Lightstream and **Xsolla Partner Network (XPN)** to find instant sponsorship opportunities and display them live.

## 🚀 Features

- **XPN Link Conversion**: Automatically converts product deals into `x.la/xpn/` shortlinks for easy typing by console viewers.
- **Lightstream Integration**: Generate a public URL using ngrok or host on Vercel to display overlays on Xbox streams.
- **Live Stream Overlay**: Professional CSS overlay that shows rotating Xbox deals with XPN branding.
- **Instant Gaming Deals**: Fetches the latest Xbox game deals from Instant Gaming (via CheapShark API).

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

### 📺 Using with Lightstream & XPN
If you are using a service that requires **XPN (x.la/xpn)** URLs:

1. **Host your Overlay**: Use Vercel (recommended) or ngrok to get a URL for your overlay.
2. **Convert to XPN**: 
   - Go to your **Xsolla Partner Dashboard**.
   - Create a new **Custom Link** pointing to your Vercel URL (e.g., `https://stream-sponsor-9ywd.vercel.app`).
   - Xsolla will provide you with an `x.la/xpn/YOUR_CODE` link.
3. **Add to Lightstream**: 
   - In Lightstream Studio, add a **Browser Source**.
   - Use the `x.la/xpn/` URL provided by Xsolla.
4. **Set Partner Code**: Set your `XSOLLA_PARTNER_CODE` environment variable so the overlay displays your specific links.

## 📋 Requirements

- Python 3.7+
- `requests`, `colorama`, `flask`, `flask-cors`, `pyngrok`

## ⚖️ Disclaimer

This tool aggregates publicly available information. While it finds opportunities that don't require sign-up to *view*, actually receiving payments or claiming rewards will eventually require you to provide a payment method (like PayPal) or create an account on the respective platform's fulfillment page.

---
*Created for Xbox Gamers.*
