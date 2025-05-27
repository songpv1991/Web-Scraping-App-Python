from PyQt5.QtCore import QThread, pyqtSignal
import requests
import time
from playwright.sync_api import sync_playwright
from config import SERVER_URL, API_PARAMS, API_HEADERS, SERVER_PAGE
from models.league import League
from alert import trigger_alert

class DataFetcher(QThread):
    data_fetched = pyqtSignal(list)
    message_alert = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.previous_data = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto(SERVER_PAGE)
            # Wait/load until odds data loads or is accessible
            page.wait_for_timeout(3000)  # you can replace with a wait_for_selector

            cookies = context.cookies()
            self.cookie_dict = {c['name']: c['value'] for c in cookies}


    def run(self):
        while True:
            self.fetch_once()
            time.sleep(1)

    def fetch_once(self):
        try:
            response = requests.get(SERVER_URL, headers = API_HEADERS, params = API_PARAMS, cookies = self.cookie_dict)
            if response.ok:
                data = response.json()
                item = self.parse_data(data)
                self.filter_changes(item)
                # self.data_fetched.emit(item)
        except Exception as e:
            print("Error fetching data:", e)


    def parse_data(self, data):
        parsed_data = []
        try:
            leagues = data["l"][0][2]
            for league in leagues:
                parsed_data.append(League(league))
        except Exception as e:
            print("Error parsing data:", e)
        return parsed_data

    def filter_changes(self, new_data):
        for prev in self.previous_data:
            for next in new_data:
                if prev.id == next.id:
                    #when league is the same id
                    for prev_match in prev.matchs:
                        for new_match in next.matchs:
                            if prev_match.id == new_match.id:

                                home_drop = (float(prev_match.odd_home_win) - float(new_match.odd_home_win)) / float(prev_match.odd_home_win) * 100
                                print(prev_match.odd_home_win, new_match.odd_home_win, home_drop)
                                if home_drop > 10:
                                    self.message_alert.emit([prev.name, prev_match.home_team, 'Home Win(1)', prev_match.odd_home_win, new_match.odd_home_win, home_drop, prev_match.start_time])

                                home_drop = (float(prev_match.odd_draw) - float(new_match.odd_draw)) / float(prev_match.odd_draw) * 100
                                print(prev_match.odd_draw, new_match.odd_draw, home_drop)
                                if home_drop > 10:
                                    self.message_alert.emit([prev.name, "Draw", 'Draw(X)', prev_match.odd_draw, new_match.odd_draw, home_drop, prev_match.start_time])

                                home_drop = (float(prev_match.odd_away_win) - float(new_match.odd_away_win)) / float(prev_match.odd_away_win) * 100
                                print(prev_match.odd_away_win, new_match.odd_away_win, home_drop)
                                if home_drop > 10:
                                    self.message_alert.emit([prev.name, prev_match.away_team, 'Away Win(1)', prev_match.odd_away_win, new_match.odd_away_win, home_drop, prev_match.start_time])

                                break
                    break
        self.previous_data = new_data