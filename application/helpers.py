#!/usr/bin/python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import re
import os
from json import dumps, loads
from random import shuffle

player_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'player_dict.json')


def create_player_dict(content):

    soup = BeautifulSoup(content, 'html.parser')
    participants_list = soup.find_all(attrs={'class': 'pww-participant'})

    player_dict = {}
    for index, player in enumerate(participants_list):
        this_player_dict = {}
        for content in player.contents:
            name_pattern = re.compile('[0-9]{1,2}. ([\w]+ [\w]+)')
            name = re.match(name_pattern, str(content))
            if name:
                this_player_dict['name'] = name.groups()[0]
            skill_pattern = re.compile('Skill: ([\w])')
            skill = re.match(skill_pattern, str(content))
            if skill:
                this_player_dict['skill'] = skill.groups()[0]
            gender_pattern = re.compile('Gender: ([\w]+)')
            gender = re.match(gender_pattern, str(content))
            if gender:
                this_player_dict['gender'] = gender.groups()[0]
        if len(this_player_dict) > 0:
            player_dict[index] = this_player_dict

    dict_length = len(player_dict)

    while len(player_dict) < 48:
        player_dict[dict_length] = {'name': '', 'gender': '', 'skill': ''}
        dict_length += 1

    with open(player_file, 'w') as outfile:
        outfile.write(dumps(player_dict))


def get_player_dict():
    with open(player_file) as infile:
        player_dict = loads(infile.read())
    return player_dict


def update_player_dict_with_rankings(rankings_per_player):
    player_dict = get_player_dict()
    for field_name, ranking in rankings_per_player.iteritems():
        id = field_name.split('_')[1]
        player = player_dict.get(id)
        player.update({'ranking': ranking})
        player_dict.update(player)
    with open(player_file, 'w') as outfile:
        outfile.write(dumps(player_dict))


def sort_players(user_data):
    player_dict = get_player_dict()
    teams = []
    one_players = []
    two_players = []
    three_players = []
    four_players = []
    for id, player in player_dict.iteritems():
        if player.get('ranking') == '1':
            one_players.append(player)





