#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
from json import loads, dumps
import os

from application.helpers import (create_player_dict,
                                 get_player_dict,
                                 sort_players,
                                 update_player_dict_with_rankings)


def create_app():
    app = Flask(import_name=__name__)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method.lower() == 'post':
            if request.form.get('participant_list'):
                create_player_dict(request.form['participant_list'])
                return redirect(url_for('player_list'))
        return render_template('home.html')

    @app.route('/player_list/', methods=['GET', 'POST'])
    def player_list():
        if request.method.lower() == 'post':
            print request.form
            update_player_dict_with_rankings(request.form)
            return 'moo'
        player_dict = get_player_dict()
        return render_template('player_list.html', player_dict=player_dict)

    return app


if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.testing = True
    app.run(port=5000)
