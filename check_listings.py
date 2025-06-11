import requests
import os
import json
from urllib.parse import urlencode

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TARGET_KEYWORD = "Jan de Oudeweg"
API_URL = "https://mosaic-plaza-aanbodapi.zig365.nl/api/v1/actueel-aanbod"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json; charset=UTF-8",
    "Referer": "https://plaza.newnewnew.space/aanbod/wonen"
}

# File to store seen titles
SEEN_TITLES_FILE = "seen_titles.txt"

def load_seen_titles():
    if os.path.exists(SEEN_TITLES_FILE):
        with open(SEEN_TITLES_FILE, 'r') as f:
            return set(f.read().splitlines())
    return set()

def save_seen_titles(titles):
    with open(SEEN_TITLES_FILE, 'w') as f:
        f.write('\n'.join(titles))

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def check_new_listings():
    try:
        seen_titles = load_seen_titles()
        found = []
        page = 0
        total_pages = None
        
        while total_pages is None or page < total_pages:
            # API parameters
            params = {
                "limit": 100,
                "locale": "nl_NL",
                "page": page,
                "sort": "+reactionData.aangepasteTotaleHuurprijs"
            }
            
            # Make the API request with URL parameters
            url = f"{API_URL}?{urlencode(params)}"
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"❌ Error: HTTP {response.status_code}")
                return

            # Parse JSON response
            data = response.json()
            
            # Save raw response for debugging (only first page)
            if page == 0:
                with open('api_response.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print("💾 Saved first page API response to api_response.json")

            # Update total pages on first iteration
            if total_pages is None and '_metadata' in data:
                total_pages = data['_metadata']['page_count']
                total_listings = data['_metadata']['total_count']
                print(f"📚 Found {total_listings} total listings across {total_pages} pages")
            
            # Process listings from the data array
            if 'data' in data:
                print(f"📃 Processing page {page + 1} of {total_pages}...")
                for listing in data['data']:
                    # Extract address details
                    street = listing.get('street', '')
                    house_number = listing.get('houseNumber', '')
                    house_number_addition = listing.get('houseNumberAddition', '').strip()
                    
                    if TARGET_KEYWORD.lower() in street.lower():
                        # Format the full address
                        listing_text = f"{street} {house_number}"
                        if house_number_addition:
                            listing_text += f" {house_number_addition}"
                        
                        if listing_text not in seen_titles:
                            print(f"\n🏠 Found new listing: {listing_text}")
                            
                            # Get additional details
                            total_rent = listing.get('totalRent', 'N/A')
                            property_type = listing.get('rentBuy', 'N/A')
                            postal_code = listing.get('postalcode', 'N/A')
                            city = listing.get('gemeenteGeoLocatieNaam', 'N/A')
                            available_from = listing.get('availableFromDate', '').split('T')[0] if listing.get('availableFromDate') else 'N/A'
                            
                            # Create the correct URL format
                            listing_id = listing.get('id', '')
                            street_slug = street.lower().replace(' ', '')
                            url = f"https://plaza.newnewnew.space/aanbod/huurwoningen/details/{listing_id}-{street_slug}-{house_number}-{city.lower()}"
                            
                            # Create detailed listing text
                            detailed_text = (
                                f"{listing_text}\n"
                                f"📍 {postal_code} {city}\n"
                                f"💰 €{total_rent}\n"
                                f"🏠 {property_type}\n"
                                f"📅 Available from: {available_from}\n"
                                f"🔗 {url}"
                            )
                            
                            seen_titles.add(listing_text)
                            found.append(detailed_text)
            
            page += 1

        if found:
            message = f"🏠 Found {len(found)} new Jan de Oudeweg listing(s):\n\n" + "\n\n".join(found)
            send_telegram_message(message)
            print(f"\n✅ Found {len(found)} new listings")
        else:
            print("\n✅ No new listings found")

        save_seen_titles(seen_titles)

    except Exception as e:
        print(f"❌ Error: {e}")
        raise e

if __name__ == "__main__":
    print("🔍 Checking listings...")
    check_new_listings()
