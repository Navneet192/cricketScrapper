from cricket_scraper.scrapers.fixtures_scraper import scrape_fixtures
from cricket_scraper.scrapers.squads_scraper import scrape_squads
import json

if __name__ == "__main__":
    fixtures = scrape_fixtures()
    if fixtures:
        for fixture in fixtures:
            print("\n[INFO] Fixture:", fixture["title"])
            print("[INFO] Match URL:", fixture["match_url"])
            squads = scrape_squads(fixture["match_url"])
            print(json.dumps(squads, indent=2, ensure_ascii=False))
    else:
        print("[ERROR] No fixtures found.") 