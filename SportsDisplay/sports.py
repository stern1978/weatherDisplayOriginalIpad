#!/usr/bin/python3

import datetime
import requests
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(__name__)

mlb_url = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard'
nhl_url = 'http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard'
epl_url = 'https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard'
uefa_champions = 'https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard'
uefa_europa = 'https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.europa/scoreboard'
club_friendly = 'https://site.api.espn.com/apis/site/v2/sports/soccer/CLUB.FRIENDLY/scoreboard'
nfl_url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

url_list = [nhl_url, nfl_url, mlb_url, uefa_champions, uefa_europa, club_friendly, epl_url]
team_list = ['NYR', 'ARS', 'MIL', 'NYY', 'GB']

@app.route('/')
def index():
    sport_dict = {}
    team_dict = {}

    for url in url_list:
      counter = 0
      url_get = requests.get(url)
      url_data = url_get.json()
      now_espn = datetime.datetime.now().strftime('%Y-%m-%dT%H:%MZ')
      if url_data['leagues'][0]['calendarEndDate'] > now_espn:
         if url_data['leagues'][0]['season']['type']['id'] != '4':
            sport_name = url_data['leagues'][0]['name']
            print(sport_name, url_data['leagues'][0]['season']['type']['id'])
            sport_dict[sport_name] = []
            for events in url_data:
               try:
                  for _ in events:
                     try:               
                        teams_playing = url_data['events'][counter]['shortName']
                        for team in team_list:
                           if team in teams_playing:
                                 home_team =  url_data['events'][counter]['competitions'][0]['competitors'][0]['team']['name']
                                 away_team =  url_data['events'][counter]['competitions'][0]['competitors'][1]['team']['name']
                                 match_status = url_data['events'][counter]['competitions'][0]['status']['type']['detail']
                                 home_score = url_data['events'][counter]['competitions'][0]['competitors'][0]['score']
                                 away_score = url_data['events'][counter]['competitions'][0]['competitors'][1]['score']
                                 home_logo = url_data['events'][counter]['competitions'][0]['competitors'][0]['team']['logo']
                                 away_logo = url_data['events'][counter]['competitions'][0]['competitors'][1]['team']['logo']
                                 game_status = url_data['events'][counter]['competitions'][0]['status']['type']['name']
                                 time = url_data['events'][counter]['date']
                                 try:
                                    channel = '- On ' + url_data['events'][counter]['competitions'][0]['broadcasts'][0]['names'][0]
                                 except:
                                    channel = ''
                                 #print(channel)
                                 team_dict[time] =[]
                                 team_dict[time].append([away_team, away_score, away_logo, home_team, home_score, home_logo, match_status, game_status, sport_name, channel])
                                 
                                 sport_dict[sport_name].append([away_team, away_score, away_logo, home_team, home_score, home_logo, match_status, game_status, time, channel])
                        counter+=1
                     except KeyError as e:
                        print(e)
               except IndexError:
                  pass   
            if not sport_dict[sport_name]:
               del sport_dict[sport_name]
    sort = dict(sorted(team_dict.items(), key=lambda item: item[0]))
    #print(sort)
    return render_template('sports.html',
    sport_dict=sort)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8012, debug=True)
