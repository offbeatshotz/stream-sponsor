import requests
import json
import os
import sys
import threading
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from colorama import init, Fore, Style
from pyngrok import ngrok, conf

# Initialize colorama for colored terminal output
init(autoreset=True)

# Flask App for Overlay
app = Flask(__name__)
CORS(app)

class XboxSponsorFinder:
    def __init__(self):
        self.cheapshark_url = "https://www.cheapshark.com/api/1.0/deals"
        self.server_thread = None
        self.public_url = None
        self.xsolla_partner_code = os.getenv("XSOLLA_PARTNER_CODE", "XPN_CREATOR") # Default code
        
        # Curated list of platforms that are "Instant Entry" or have public bounties
        self.instant_platforms = [
            {
                "name": "Xsolla Partner Network (XPN)",
                "benefit": "Get paid for playing games with trackable x.la/xpn links.",
                "link": "https://x.la/xpn/",
                "type": "XPN Sponsorship"
            },
            {
                "name": "Lightstream Studio",
                "benefit": "Add overlays to Xbox streams without a PC/Capture Card.",
                "link": "https://www.golightstream.com/xbox/",
                "type": "Stream Tool"
            },
            {
                "name": "StreamElements Sponsorships",
                "benefit": "Pre-approved campaigns for Twitch/YouTube (0+ viewers).",
                "link": "https://streamelements.com/dashboard/sponsorships",
                "type": "Stream Service"
            },
            {
                "name": "Kick Affiliate Program",
                "benefit": "Lower entry bar for revenue share on Kick.com.",
                "link": "https://kick.com/creator-program",
                "type": "Stream Service"
            },
            {
                "name": "Lurkit Quest Board",
                "benefit": "Public board for game keys and paid bounties.",
                "link": "https://www.lurkit.com/quests",
                "type": "Bounty"
            }
        ]

    def get_xpn_url(self, title):
        """Generates a clean XPN-style shortlink for the overlay."""
        # Clean title for SKU-style URL
        sku = "".join(filter(str.isalnum, title)).upper()[:10]
        return f"x.la/xpn/{self.xsolla_partner_code}/{sku}"

    def get_xbox_deals(self, limit=5):
        """Fetches current Xbox deals and attaches XPN shortlinks."""
        params = {
            "upperPrice": 60,
            "pageSize": limit,
            "title": "Xbox"
        }
        
        try:
            response = requests.get(self.cheapshark_url, params=params, timeout=10)
            if response.status_code == 200:
                deals = response.json()
                for deal in deals:
                    deal['xpn_url'] = self.get_xpn_url(deal['title'])
                return deals
            else:
                return []
        except Exception:
            return []

    def start_overlay_server(self):
        if self.server_thread and self.server_thread.is_alive():
            print(f"{Fore.YELLOW}Overlay server is already running.")
            if self.public_url:
                print(f"{Fore.MAGENTA}Public URL: {self.public_url}")
            return

        print(f"\n{Fore.CYAN}--- Stream Overlay Configuration ---")
        print(f"{Fore.WHITE}To use with Lightstream (Xbox), you need a public URL.")
        print(f"{Fore.WHITE}You can get a free token at {Fore.YELLOW}https://dashboard.ngrok.com/get-started/your-authtoken")
        
        auth_token = input(f"\n{Fore.YELLOW}Enter ngrok auth token (leave blank for Local Only): ").strip()
        
        def run_flask():
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            app.run(port=5000, debug=False, use_reloader=False)

        self.server_thread = threading.Thread(target=run_flask, daemon=True)
        self.server_thread.start()
        
        print(f"\n{Fore.GREEN}Local Server started at http://localhost:5000")
        
        if auth_token:
            try:
                ngrok.set_auth_token(auth_token)
                self.public_url = ngrok.connect(5000).public_url
                print(f"{Fore.MAGENTA}LIGHTSTREAM PUBLIC URL: {Fore.WHITE}{self.public_url}")
                print(f"{Fore.YELLOW}Copy this URL into your Lightstream Browser Source Layer.")
            except Exception as e:
                print(f"{Fore.RED}Ngrok Error: {e}")
                print(f"{Fore.YELLOW}Falling back to Local Only mode.")

    def display_header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.GREEN}{Style.BRIGHT}" + "="*50)
        print(f"{Fore.GREEN}{Style.BRIGHT}   XBOX, LIGHTSTREAM & STREAM FINDER")
        print(f"{Fore.GREEN}{Style.BRIGHT}" + "="*50)
        print(f"{Fore.YELLOW}Get paid for Xbox streaming via Twitch/YouTube!")
        if self.server_thread and self.server_thread.is_alive():
            status = f"PUBLIC: {self.public_url}" if self.public_url else "LOCAL ONLY"
            print(f"{Fore.MAGENTA}[OVERLAY ACTIVE] {status}")
        print("="*50 + "\n")

    def show_menu(self):
        print(f"{Fore.WHITE}1. {Fore.CYAN}Find High-Value Xbox Deals (Affiliate)")
        print(f"{Fore.WHITE}2. {Fore.CYAN}Browse Lightstream & Sponsor Platforms")
        print(f"{Fore.WHITE}3. {Fore.CYAN}Search for Open Gaming Bounties")
        print(f"{Fore.WHITE}4. {Fore.MAGENTA}Setup Lightstream/OBS Overlay")
        print(f"{Fore.WHITE}5. {Fore.RED}Exit")
        return input(f"\n{Fore.YELLOW}Select an option: ")

    def run_deals(self):
        print(f"{Fore.CYAN}Searching for current Xbox deals...")
        deals = self.get_xbox_deals(limit=8)
        if not deals:
            print(f"{Fore.RED}No deals found at the moment.")
        else:
            print(f"\n{Fore.GREEN}Top Xbox Deals to Promote (Affiliate Opportunity):")
            for deal in deals:
                savings = float(deal['savings'])
                color = Fore.GREEN if savings > 50 else Fore.WHITE
                print(f"{color}• {deal['title']}")
                print(f"  Price: ${deal['salePrice']} (Reg: ${deal['normalPrice']}) - {savings:.0f}% OFF")
                print(f"  Link: https://www.instant-gaming.com/en/search/?q={deal['title'].replace(' ', '+')}")
                print("-" * 30)
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...")

    def run_platforms(self):
        print(f"\n{Fore.GREEN}Instant/Easy-Entry Platforms for Xbox & Streamers:")
        for p in self.instant_platforms:
            print(f"{Fore.CYAN}[{p['type']}] {Fore.WHITE}{p['name']}")
            print(f"  Benefit: {p['benefit']}")
            print(f"  Link: {p['link']}")
            print("-" * 30)
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...")

    def run_bounties(self):
        print(f"\n{Fore.MAGENTA}Searching for Open Quests & Bounties...")
        bounties = [
            {"name": "Xbox FanFest Bounties", "url": "https://www.xbox.com/en-US/fanfest"},
            {"name": "Microsoft Rewards (Paid for playing)", "url": "https://www.microsoft.com/en-us/rewards/xbox"},
            {"name": "Buff.game (Passive income while playing)", "url": "https://buff.game/"},
            {"name": "Repeat.gg (Xbox Tournaments/Bounties)", "url": "https://www.repeat.gg/"}
        ]
        
        for b in bounties:
            print(f"{Fore.WHITE}• {Fore.CYAN}{b['name']}")
            print(f"  Check here: {b['url']}")
            print("-" * 30)
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...")

    def main(self):
        while True:
            self.display_header()
            choice = self.show_menu()
            
            if choice == '1':
                self.run_deals()
            elif choice == '2':
                self.run_platforms()
            elif choice == '3':
                self.run_bounties()
            elif choice == '4':
                self.start_overlay_server()
                input(f"\n{Fore.YELLOW}Press Enter to return to menu...")
            elif choice == '5':
                print(f"{Fore.GREEN}Good luck with your stream! Goodbye.")
                break
            else:
                print(f"{Fore.RED}Invalid selection. Try again.")

# Global instance for Vercel and routes
finder = XboxSponsorFinder()

@app.route('/')
def overlay():
    return render_template('overlay.html')

@app.route('/api/deals')
def api_deals():
    return jsonify(finder.get_xbox_deals(limit=5))

if __name__ == "__main__":
    try:
        finder.main()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Exiting...")
        sys.exit()
