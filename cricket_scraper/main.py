
from scrapers.fixtures_scraper import scrape_fixtures

def main():
    fixtures = scrape_fixtures()
    print(f"[INFO] Found {len(fixtures)} fixtures")
    for match in fixtures:
        print(match)

if __name__ == "__main__":
    main()