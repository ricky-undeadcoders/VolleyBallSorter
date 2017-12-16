#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2

conn_string = "host='localhost' dbname='VolleyBallSorter' user='postgres' password='admin'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

try:
    cursor.execute("DROP TABLE players")
    conn.commit()
except Exception as e:
    print('Players table didn\'t exist')
    conn.rollback()
try:
    cursor.execute("SELECT * FROM team")
    cursor.execute("DROP TABLE team")
    conn.commit()
except Exception as e:
    print('Team table didn\'t exist')
    conn.rollback()

cursor.execute(
    "CREATE TABLE team (team_id serial PRIMARY KEY, team_name VARCHAR(20))")
cursor.execute(
    "CREATE TABLE players(player_id serial PRIMARY KEY, name VARCHAR(20), skill VARCHAR(1), gender VARCHAR(10), team_id integer, FOREIGN KEY (team_id) REFERENCES team(team_id))")
conn.commit()
