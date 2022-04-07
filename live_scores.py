import requests
from bs4 import BeautifulSoup

class User:
  def __init__(self, n, one, two, three, ts):
    self.name = n
    self.firstPick = one
    self.secondPick = two
    self.thirdPick = three
    self.team_score = ts

class Player:
  def __init__(self, n, s, t):
    self.name = n
    self.score = s
    self.thru = t

users = []
users.append(User("Mary Jane","Cameron Smith","Max Homa","Tyrrell Hatton",0))
users.append(User("Jovon","Justin Thomas","Justin Rose","Sungjae Im",0))
users.append(User("Jalen","Jon Rahm","Shane Lowry","Marc Leishman",0))
users.append(User("Quinn","Collin Morikawa","Tommy Fleetwood","Harold Varner III",0))
users.append(User("Voyles","Brooks Koepka","Sam Burns","Cameron Champ",0))
users.append(User("Beeb","Xander Schauffele","Patrick Reed","Daniel Berger",0))
users.append(User("JJ","Scottie Scheffler","Russell Henley","Bryson DeChambeau",0))
users.append(User("Tyler","Dustin Johnson","Jordan Spieth","Talor Gooch",0))
users.append(User("Gabe","Tiger Woods","Hideki Matsuyama","Thomas Pieters",0))
users.append(User("Dylan","Matthew Wolff","Rory McIlroy","Harry Higgs",0))
users.append(User("Paul","Viktor Hovland","Joaquin Niemann","Patrick Cantlay",0))
users.append(User("Alek","Tony Finau","Si Woo Kim","Corey Conners",0))
users.append(User("Bill","Billy Horschel","Abraham Ancer","Matt Fitzpatrick",0))
users.append(User("Christian","Louis Oosthuizen","Will Zalatoris","Adam Scott",0))

def get_players(soup, player_col, score_col, thru_col):
    rows = soup.find_all("tr", class_="PlayerRow__Overview PlayerRow__Overview--expandable Table__TR Table__even")
    players = []
    for row in rows[0:]:
        cols = row.find_all("td")
        # If we get a bad row. For example, during the tournament we there 
        # is a place holder row that represents the cut line
        if len(cols) < 5:
            continue
        player = cols[player_col].text.strip()
        score = cols[score_col].text.strip().upper()        
        thru = cols[thru_col].text.strip() if thru_col else "F" 
        if score == 'CUT':
            score_final = 'CUT'
            continue
        elif score == 'WD':
            score_final = 'WD'
            continue
        elif score == 'DQ':
            score_final = 'DQ'
            continue
        elif score == 'E':
            score_final = 0
        else:
            try:
                score_final = int(score)
            except ValueError:
                score_final = '?'

        players.append(Player(player,score_final,thru))

    return players

def get_col_indecies(soup):
    header_rows = soup.find_all("tr", class_="Table__TR Table__even")
    
    # other possible entries for what could show up, add here.
    player_fields = ['PLAYER']
    to_par_fields = ['TO PAR', 'TOPAR', 'TO_PAR', 'SCORE']
    thru_fields = ['THRU']
    header_col = header_rows[0].find_all("th")
    player_col = None
    score_col = None
    thru_col = None
    for i in range(len(header_col)):
        col_txt = header_col[i].text.strip().upper()
        if col_txt in player_fields:
            player_col = i
            continue
        if col_txt in to_par_fields:
            score_col = i
            continue
        if col_txt in thru_fields:
            thru_col = i
            continue
    if player_col is None or score_col is None:
        print("Unable to track columns")
        exit()
    
    return player_col, score_col, thru_col

def verify_scrape(players):
    if len(players) < 25:
        print("Less than 25 players, seems suspucious, so exiting")
        exit()
    bad_entry_count = 0
    bad_score_count = 0
    for key, value in players.items():
        scr = players[key]['TO PAR']
        if scr == '?':
            bad_entry_count += 1
        if type(scr) is int and (scr > 50 or scr < -50):
            print("Bad score entry, exiting")
            exit()
    if bad_entry_count > 3:
        # arbitrary number here, I figure this is enough bad entries to call it a bad pull
        print("Multiple bad entries, exiting")
        exit()

def get_tournament_name(soup):
    tournament_name = soup.find_all("h1", class_="headline headline__h1 Leaderboard__Event__Title")[0].text
    return tournament_name

def get_player_score(name):
    
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    player_col, score_col, thru_col = get_col_indecies(soup)
    players = get_players(soup, player_col, score_col, thru_col)

    for player in players:
        if(player.name == name):
            string_score = player.name + " is " + str(player.score) + " thru " + player.thru
            return string_score

def users_scores(name):
    
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    player_col, score_col, thru_col = get_col_indecies(soup)
    players = get_players(soup, player_col, score_col, thru_col)
    string_score = ""
    for user in users:
        if user.name == name:
            for player in players:
                if(user.firstPick == player.name):
                    string_score = player.name + " is " + str(player.score) + " thru " + player.thru + "\n"
                    user.team_score = player.score
            for player in players:
                if(user.secondPick == player.name):
                    string_score += player.name + " is " + str(player.score) + " thru " + player.thru + "\n"
                    user.team_score += player.score
            for player in players:
                if(user.thirdPick == player.name):
                    string_score += player.name + " is " + str(player.score) + " thru " + player.thru + "\n"
                    user.team_score += player.score
    
            string_score += "Your Score is " + str(user.team_score)

    return string_score

def update_scores():
    
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    player_col, score_col, thru_col = get_col_indecies(soup)
    players = get_players(soup, player_col, score_col, thru_col)
    for user in users:
        for player in players:
            if(user.firstPick == player.name):
                user.team_score = player.score
        for player in players:
            if(user.secondPick == player.name):
                user.team_score += player.score
        for player in players:
            if(user.thirdPick == player.name):
                user.team_score += player.score


def get_leaderboard():
    update_scores()
    users.sort(key=lambda x: x.team_score)
    
    leaderboard_string = ""
    index = 1
    for user in users:
        if index == 14:
            leaderboard_string += (str(index) + ": " + user.name + " @ " + str(user.team_score))
        else:
            leaderboard_string += (str(index) + ": " + user.name + " @ " + str(user.team_score) + "\n")

        index = index + 1

    return leaderboard_string