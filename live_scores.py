import requests
from bs4 import BeautifulSoup

class User:
  def __init__(self, n, one, two, three, four, ts):
    self.name = n
    self.firstPick = one
    self.secondPick = two
    self.thirdPick = three
    self.fourthPick = four
    self.team_score = ts

class Player:
  def __init__(self, n, s, t):
    self.name = n
    self.score = s
    self.thru = t

COURSE_PAR = 71
TOURNAMENT_CUT = 143

users = []
users.append(User("Quinn","Rory McIlroy","Hideki Matsuyama","Robert MacIntyre","Branden Grace",0))
users.append(User("Dylan","Scottie Scheffler","Wyndham Clark","Brian Harman","J.T. Poston",0))
users.append(User("Bill","Jon Rahm","Sam Burns","Keegan Bradley","Billy Horschel",0))
users.append(User("Beeb","Brooks Koepka","Talor Gooch","Jason Day","Thomas Pieters",0))
users.append(User("Matt","Cameron Smith","Jordan Spieth","Cameron Young","Nicolai Højgaard",0))
users.append(User("Ramsey","Xander Schauffele","Justin Rose","Patrick Reed","Harris English",0))
users.append(User("Liam","Viktor Hovland","Shane Lowry","Corey Conners","Louis Oosthuizen",0))
users.append(User("Tyler","Tyrrell Hatton","Patrick Cantlay","Denny McCarthy","Joaquin Niemann",0))
users.append(User("Jovon","Collin Morikawa","Rickie Fowler","Min Woo Lee","Russell Henley",0))
users.append(User("Paul","Justin Thomas","Bryson DeChambeau","Sepp Straka","Padraig Harrington",0))
users.append(User("JJ","Tommy Fleetwood","Tony Finau","Sungjae Im","Ryan Fox",0))
users.append(User("Christian","Matt Fitzpatrick","Tom Kim","Kurt Kitayama","Zach Johnson",0))
users.append(User("Ryan","Dustin Johnson","Max Homa","Sahith Theegala","Si Woo Kim",0))

def get_players(soup, player_col, score_col, thru_col, round_one_col):
    rows = soup.find_all("tr", class_="PlayerRow__Overview PlayerRow__Overview--expandable Table__TR Table__even")
    players = []
    for row in rows[0:]:
        cols = row.find_all("td")
        # If we get a bad row. For example, during the tournament there 
        # is a place holder row that represents the cut line
        if len(cols) < 5:
            continue
        player = cols[player_col].text.strip()
        score = cols[score_col].text.strip().upper()        
        thru = cols[thru_col].text.strip() if thru_col else "F" 
        total_score = 0
        score_found = False
        x = 0
        if score == 'CUT':
            while score_found == False:
                round_score = cols[round_one_col + x].text.strip()
                total_score = total_score + int(round_score)
                if (cols[round_one_col + x + 1].text.strip()) == "--":
                    score_final = total_score - COURSE_PAR * (x+1)
                    score_final = score_final + (total_score - TOURNAMENT_CUT) * 2
                    score_found = True
                x = x + 1
        elif score == 'WD':
            while score_found == False:
                round_score = cols[round_one_col + x].text.strip()
                if round_score != "--":
                    total_score = total_score + int(round_score)
                    if (cols[round_one_col + x + 1].text.strip()) == "--":
                        score_final = total_score - COURSE_PAR * (x+1)
                        score_found = True
                    x = x + 1
                else:
                    score_final = 0
                    score_found = True
        elif score == 'DQ':
            while score_found == False:
                round_score = cols[round_one_col + x].text.strip()
                total_score = total_score + int(round_score)
                if (cols[round_one_col + x + 1].text.strip()) == "--":
                    score_final = total_score - COURSE_PAR * (x+1)
                    score_found = True
                x = x + 1
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
    round_one_fields = ["R1"]
    header_col = header_rows[0].find_all("th")
    player_col = None
    score_col = None
    thru_col = None
    round_one_col = None
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
        if col_txt in round_one_fields:
            round_one_col = i
    if player_col is None or score_col is None:
        print("Unable to track columns")
        exit()
    
    return player_col, score_col, thru_col, round_one_col

def get_tournament_name(soup):
    tournament_name = soup.find_all("h1", class_="headline headline__h1 Leaderboard__Event__Title")[0].text
    return tournament_name

def get_player_score(name):
    
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    player_col, score_col, thru_col, round_one_col = get_col_indecies(soup)
    players = get_players(soup, player_col, score_col, thru_col, round_one_col)

    for player in players:
        if(player.name == name):
            string_score = player.name + " is " + str(player.score) + " thru " + player.thru
            return string_score

def users_scores(name):
    
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    player_col, score_col, thru_col, round_one_col = get_col_indecies(soup)
    players = get_players(soup, player_col, score_col, thru_col, round_one_col)
    string_score = ""
    worst_score = -100
    worst_player = ""
    for user in users:
        if user.name.lower() == name.lower():
            for player in players:
                if(user.firstPick == player.name):
                    string_score = player.name + " is " + str(player.score) + " thru " + player.thru + "\n"
                    user.team_score = player.score
                    if player.score > worst_score:
                        worst_score = player.score
                        worst_player = player.name
            for player in players:
                if(user.secondPick == player.name):
                    string_score += player.name + " is " + str(player.score) + " thru " + player.thru + "\n"
                    user.team_score += player.score
                    if player.score > worst_score:
                        worst_score = player.score
                        worst_player = player.name
            for player in players:
                if(user.thirdPick == player.name):
                    string_score += player.name + " is " + str(player.score) + " thru " + player.thru + "\n"
                    user.team_score += player.score
                    if player.score > worst_score:
                        worst_score = player.score
                        worst_player = player.name
            for player in players:
                if(user.fourthPick == player.name):
                    string_score += player.name + " is " + str(player.score) + " thru " + player.thru + "\n"
                    user.team_score += player.score
                    if player.score > worst_score:
                        worst_score = player.score
                        worst_player = player.name

            string_score += worst_player + " score is dropped" + "\n"
            user.team_score = user.team_score - worst_score
    
            string_score += "Your Score is " + str(user.team_score)

    return string_score

def update_scores():
    
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    player_col, score_col, thru_col, round_one_col = get_col_indecies(soup)
    players = get_players(soup, player_col, score_col, thru_col, round_one_col)
    for user in users:
        worst_score = -100
        for player in players:
            if(user.firstPick == player.name):
                user.team_score = player.score
                if player.score > worst_score:
                    worst_score = player.score
        for player in players:
            if(user.secondPick == player.name):
                user.team_score += player.score
                if player.score > worst_score:
                    worst_score = player.score
        for player in players:
            if(user.thirdPick == player.name):
                user.team_score += player.score
                if player.score > worst_score:
                    worst_score = player.score
        for player in players:
            if(user.fourthPick == player.name):
                user.team_score += player.score
                if player.score > worst_score:
                    worst_score = player.score

        user.team_score = user.team_score - worst_score


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