from models.market import Market
class Match:
    def __init__(self, match):
        self.id = match[0]
        self.home_team = match[1]
        self.away_team = match[2]
        self.start_time = match[4]
        self.markets = []
        market = match[8]["0"]

        # Handicap
        handicap_market = market[0][0] or ['','','']
        self.handicap_line = handicap_market[2] or ''
        self.home_odd = handicap_market[3] or ''
        self.away_odd = handicap_market[4] or ''
        
        # Over/Under
        ou_market = market[1][0] or ['','','']
        self.ou_line = ou_market[0] or ''
        self.over_odd = ou_market[2] or ''
        self.under_odd = ou_market[3] or ''

        # 1X2
        one_x_two = market[2] or ['','','']
        self.odd_home_win = one_x_two[0] or ''
        self.odd_draw = one_x_two[1] or ''
        self.odd_away_win = one_x_two[2] or ''