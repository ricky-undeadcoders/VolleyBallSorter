#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2

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
    return_list = []
    columns = [desc[0] for desc in cursor.description]
    for data in cursor.fetchall():
        player_dict = {}
        for id, value in enumerate(data):
            player_dict.update({columns[id]: value})
        return_list.append(player_dict)

    return return_list


def create_team(player_ids, team_id):
    for player_id in player_ids:
        cursor.execute("SELECT add_team_player({{}, {}})".format(player_id, team_id))
        conn.commit()
    return True
