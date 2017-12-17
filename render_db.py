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
    cursor.execute("DROP TABLE team")
    conn.commit()
except Exception as e:
    print('Team table didn\'t exist')
    conn.rollback()

cursor.execute(
    "CREATE TABLE team (team_id serial PRIMARY KEY, team_name VARCHAR(20))")
cursor.execute(
    "CREATE TABLE players(player_id serial PRIMARY KEY, name VARCHAR(20), skill VARCHAR(1), gender VARCHAR(10), team_id INTEGER, ranking INTEGER, FOREIGN KEY (team_id) REFERENCES team(team_id))")
conn.commit()

try:
    add_player = \
        '''
    CREATE OR REPLACE FUNCTION public.add_player(
        name text,
        skill text,
        gender text)
      RETURNS integer AS
    $BODY$
        INSERT INTO players (name, skill, gender) VALUES (name, skill, gender);
        SELECT player_id from players where name = name;
    $BODY$
      LANGUAGE sql VOLATILE
      COST 100;
    ALTER FUNCTION public.add_player(text, text, text)
      OWNER TO postgres;
        '''
    cursor.execute(add_player)
    conn.commit()
except Exception as e:
    print("Unable to add player", e)
    conn.rollback()


