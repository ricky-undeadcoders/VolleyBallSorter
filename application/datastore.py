#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from random import shuffle

conn_string = "host='localhost' dbname='VolleyBallSorter' user='postgres' password='admin'"
conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


def create_player(name, skill=None, gender=None):
    inserts = "'{}'".format(name)
    if skill:
        inserts += ", '{}'".format(skill)
    if gender:
        inserts += ", '{}'".format(gender)
    cursor.execute("SELECT add_player({})".format(inserts))
    conn.commit()
    return True


def find_all_players():
    cursor.execute('SELECT * FROM players')
    player_dict = {}
    columns = [desc[0] for desc in cursor.description]
    for data in cursor.fetchall():
        this_player_dict = {}
        player_id = -1
        for id, value in enumerate(data):
            if columns[id] == 'player_id':
                player_id = value
            this_player_dict.update({columns[id]: value})
        player_dict[player_id] = this_player_dict
    return player_dict


def find_all_teams():
    players = find_all_players()
    cursor.execute('SELECT * FROM team')
    team_dict = {}
    columns = [desc[0] for desc in cursor.description]
    for data in cursor.fetchall():
        team_dict[data[0]] = {}
    for id, player in players.items():
        if player[id]


def create_team(player_ids):
    cursor.execute("INSERT INTO team (team_name) VALUES ('mooky');")
    conn.commit()
    cursor.execute('SELECT team_id from team LIMIT 1')
    team_id = cursor.fetchone()[0]
    for player_id in player_ids:
        cursor.execute("UPDATE players SET team_id = {} WHERE player_id = {}".format(team_id, player_id))
        conn.commit()
    return True


def update_player_rankings(rankings_per_player):
    for field_name, ranking in rankings_per_player.items():
        id = field_name.split('_')[1]
        cursor.execute('UPDATE players SET ranking= {} WHERE player_id = {}'.format(ranking, id))
        conn.commit()


def sort_players():
    player_dict = find_all_players()
    teams = []
    one_players = []
    two_players = []
    three_players = []
    four_players = []
    for id, player in player_dict.items():
        if player.get('ranking') == 1:
            one_players.append(player)
        if player.get('ranking') == 2:
            two_players.append(player)
        if player.get('ranking') == 3:
            three_players.append(player)
        if player.get('ranking') == 4:
            four_players.append(player)
    for i in range(12):
        shuffle(one_players)
        shuffle(two_players)
        shuffle(three_players)
        shuffle(four_players)
        cursor.execute("INSERT INTO team (team_name) VALUES ('oogah') RETURNING team_id")
        team_id = cursor.fetchone()[0]
        conn.commit()
        onezy = one_players.pop()
        twozy = two_players.pop()
        threezy = three_players.pop()
        fourzy = four_players.pop()

        cursor.execute("UPDATE players SET team_id = {} WHERE player_id = {}".format(team_id, onezy['player_id']))
        conn.commit()
        cursor.execute("UPDATE players SET team_id = {} WHERE player_id = {}".format(team_id, twozy['player_id']))
        conn.commit()
        cursor.execute("UPDATE players SET team_id = {} WHERE player_id = {}".format(team_id, threezy['player_id']))
        conn.commit()
        cursor.execute("UPDATE players SET team_id = {} WHERE player_id = {}".format(team_id, fourzy['player_id']))
        conn.commit()
    return teams
