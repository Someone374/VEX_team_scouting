import requests,json,getpass
from config import *
import pandas as pd
import numpy as np
import time

# This is an open source application developed by VEX V5 team 23382H

def get_events_by_sku(event_sku):
    # sample sku:  "RE-VRC-23-4112"
    url = base_url + "/events?"+"sku[]="+event_sku+"&myEvents=false"
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}    
    r = requests.request("GET",url, headers=headers, data=payload)
    print(r.json())
    return r.json()['data']


def get_teams_by_event_id(event_id):
    url = base_url + "/events/"+ event_id +"/teams?per_page=500"
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}    
    r = requests.request("GET",url, headers=headers, data=payload)
    return r.json()['data']

def get_teams_by_state(state):
    url = 'https://www.robotevents.com/api/v2/teams?registered=true&program%5B%5D=1&grade%5B%5D=Middle%20School&country%5B%5D=US&myTeams=false'
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}    
    r = requests.request("GET",url, headers=headers, data=payload)    
    return r.json()['data']

def get_events_by_team(event_id,season):
    url = base_url + "/teams/"+ event_id+"/events/?season%5B%5D="+season
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}    
    r = requests.request("GET",url, headers=headers, data=payload)
    return r.json()['data']  

def get_team_id_by_number(number):
    url = base_url + "/teams?number%5B%5D="+ number +"&registered=true&program%5B%5D=1&grade%5B%5D=Middle%20School&country%5B%5D=US&myTeams=false"
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}    
    r = requests.request("GET",url, headers=headers, data=payload)
    return r.json()['data'][0]    

def get_awards_by_team(team_id):
    url = base_url + "/teams/"+ team_id +"/awards"
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}    
    r = requests.request("GET",url, headers=headers, data=payload)
    return r.json()['data']   

def format_awards(awards):
    list_awards = []
    for awd in awards:
        summary = awd['title']+"       "+str(awd['event']['id'])+awd['event']['name']
        list_awards.append(summary)    
    return(list_awards)

def get_skill_by_team(team_id,skill_type='driver',season='190'):
    #skill_type:  driver, programming
    url = base_url +'/teams/'+team_id +'/skills?type%5B%5D='+skill_type+'&season%5B%5D='+ season
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}
    try:
        r = requests.request("GET",url, headers=headers, data=payload)
        return r.json()['data'] 
    except:
        return([])
     

def format_skill(list_skill):
    max_score = 0
    venue = ''
    for skill in list_skill:
        if skill['score']>max_score:
            max_score = skill['score']
            venue = skill['event']['name']
    return(str(max_score))

def get_matches_by_team_and_event(event_id,team_id,div="1"):
    url = base_url + "/events/"+ event_id +"/divisions/"+div+"/matches?team%5B%5D="+team_id
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    payload = {}    
    r = requests.request("GET",url, headers=headers, data=payload)
    return r.json()['data']

def format_match(list_matches):
    matches_of_season = []
    if list_matches != []:
        for match in list_matches:
            if match["started"] is not None:
                combat = match['name']+"    "+str(match['event']['id'])+"    "+match["event"]["name"]+ "    "+match["started"]
                matches_of_season.append(combat)
        return(matches_of_season)
    else:
        return('')
    
def parse_tournament_statistics(rankings):
    event_list = []
    for evnt in rankings['data']:
        #event_json = evnt['event']+evnt['rank']+evnt['event']
        event_list.append(evnt)
    team_event_df = pd.DataFrame(event_list)
    return team_event_df

def get_tournament_statistics_by_team_by_season(team_id,season='190'):
    url = base_url + "/teams/"+team_id+"/rankings"
    params = {
        'id':team_id,
        'season':season
    }
    headers = { 
        "Authorization" : token,
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }  
    r = requests.request("GET",url, headers=headers, params=params)
    team_event_df = parse_tournament_statistics(r.json())
    return team_event_df
    
