import requests
from bs4 import BeautifulSoup
from cricket_scraper.config import HEADERS
from urllib.parse import urljoin
import re

def scrape_squads(match_url):
    base_url = re.sub(r'/(live|scorecard)$', '', match_url.rstrip('/'))
    info_url = base_url + "/info"
    print(f"[INFO] Requesting squads from: {info_url}")
    try:
        response = requests.get(info_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch squads page: {e}")
        return None

    soup = BeautifulSoup(response.text, "lxml")

    squads = {'team1': {'name': '', 'playing_xi': []}, 'team2': {'name': '', 'playing_xi': []}}
    try:
        team_headers = soup.select('div.playing-xi-container .team-header, .playing-xi-container .team-name')
        if not team_headers or len(team_headers) < 2:
            team_headers = soup.select('.team-name')
        team_blocks = soup.select('div.playing-xi-container')
        if not team_blocks or len(team_blocks) < 2:
            team_blocks = soup.select('.playing-xi')
        for i in range(2):
            if team_headers and len(team_headers) > i:
                squads[f'team{i+1}']['name'] = team_headers[i].get_text(strip=True)
            if team_blocks and len(team_blocks) > i:
                player_tags = team_blocks[i].select('.player-name, .player')
                if not player_tags:
                    player_tags = team_blocks[i].find_all('span')
                squads[f'team{i+1}']['playing_xi'] = [p.get_text(strip=True) for p in player_tags if p.get_text(strip=True)]
    except Exception as e:
        print(f"[ERROR] Error parsing squads: {e}")
        return None

    return squads
