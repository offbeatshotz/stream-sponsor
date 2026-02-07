from xbox_sponsor_finder import XboxSponsorFinder

def test_deals():
    finder = XboxSponsorFinder()
    print("Testing with Xbox title filter across all stores...")
    deals = finder.get_xbox_deals(limit=5)
    if deals:
        print(f"Success: Found {len(deals)} Xbox deals.")
        for d in deals:
            print(f"- {d['title']} at ${d['salePrice']}")
    else:
        print("No Xbox deals found at the moment.")

test_deals()
