import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from cricket_scraper.config import FIXTURES_URL, BASE_URL, HEADERS

def scrape_fixtures():
    print(f"[INFO] Requesting: {FIXTURES_URL}")
    try:
        response = requests.get(FIXTURES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch page: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    match_cards = soup.select(".match-card-container")
    print(f"[INFO] Found {len(match_cards)} match cards")

    fixtures = []
    for card in match_cards:
        link_tag = card.find("a", class_="match-card-wrapper", href=True)
        match_details = card.find("div", class_="match-details")
        team_names = [span.text.strip() for span in card.select(".team-name")]
        time_tag = card.find("div", class_="start-text")
        match_time = time_tag.text.strip() if time_tag else None
        title = " vs ".join(team_names) if len(team_names) == 2 else None
        match_data = {
            "title": title,
            "match_url": urljoin(BASE_URL, link_tag["href"]) if link_tag else None,
            "start_time": match_time
        }
        fixtures.append(match_data)

    return fixtures