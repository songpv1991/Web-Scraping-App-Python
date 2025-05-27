from datetime import datetime
from models.match import Match
class League:
    def __init__(self, league):
        self.id = league[0]
        self.name = league[1]
        self.matchs = []
        matchs = league[2]
        for match in matchs:
            self.matchs.append(Match(match))

    def toArray(self):
        array = []
        for match in self.matchs:
            item = []
            item.append(self.name)
            item.append(match.home_team)
            item.append(match.away_team)
            item.append(match.handicap_line + "\n" + match.home_odd + "\n" + match.away_odd)
            item.append(match.ou_line  + "\n" + match.over_odd  + "\n" + match.under_odd)
            item.append(match.odd_home_win  + "\n" + match.odd_draw  + "\n" + match.odd_away_win)
            dt = datetime.fromtimestamp(int(match.start_time)/1000)
            item.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
            array.append(item)
        return array
