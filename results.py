#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:si:et:enc=utf-8

# Author: Hauke Petersen <devel@haukepetersen.de>
#
# This file is part of kneipenskat.
#
# kneipenskat is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# kneipenskat is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with kneipenskat; see the file COPYING3.  If not see
# <http://www.gnu.org/licenses/>.


import re
import json
import copy
import argparse
import matplotlib.pyplot as plt
import numpy as np

title_prefix = "Kneipenskatturnier 2018 (Berlin) - "

def list_barnames(db):
    res = []
    for bar in db['bars']:
        res.append(bar['name'])
    return res

def barchart(title, labels, x, y):
    y_pos = np.arange(len(x))

    fig, ax = plt.subplots()
    for i, v in enumerate(y):
        if v < 0.0:
            hpos = (v / 2) + (v / 2 * 0.1)
        else:
            hpos = (v / 2) - (v / 2 * 0.1)
        ax.text(i - 0.2, hpos, str(v))

    ax.bar(y_pos, y, align='center', alpha=0.5)
    plt.xticks(y_pos, x)
    ax.autoscale_view()

    plt.title("{}{}".format(title_prefix, title))
    plt.xlabel(labels['x'], labelpad=140)
    plt.ylabel(labels['y'])
    fig.autofmt_xdate()

    plt.show()
    # plt.savefig(os.path.join('test.pdf'), dpi=300, format='pdf', bbox_inches='tight') #


def linechart(title, labels, x, y_data, y_labels):
    # vertical lines...
    # xcoords = [0.1, 0.3, 0.5]
    # colors = ['r','k','b']

    # for xc,c in zip(xcoords,colors):
    #     plt.axvline(x=xc, label='line at x = {}'.format(xc), c=c)

    # y_pos = np.arrange(len(data['x']))

    for i, line in enumerate(y_data):
        plt.plot(x, line, label=y_labels[i])

    plt.title("{}{}".format(title_prefix, title))
    plt.xlabel(labels['x'])
    plt.ylabel(labels['y'])
    plt.legend(fontsize=8)
    plt.margins(x=0)
    plt.show()




def analyze_overall_points(db):
    title = "Amtliches Endergebnis"
    labels = { 'x': "Spieler", 'y': "Punkte" }

    points = [0, 0, 0, 0, 0 ,0]
    for bar in db['bars']:
        for paper in bar['paper']:
            pmap = paper['players'];
            for game in paper['games']:
                points[pmap[game[1]]] += game[0]

    print("muh", db['players'])
    barchart(title, labels, db['players'], points)


def analyze_point_tracking(db):
    title = "Punkteentwicklung"
    labels = { 'x': "Spiele", 'y': "Punkte" }

    pos = 1
    games = [0]
    history = []
    points = [0] * len(db['players'])

    for i in range(len(db['players'])):
        history.append([0])

    for bar in db['bars']:

        paper = bar['paper']
        pmap = [paper[0]['players'], paper[1]['players']]

        for i in range(max([len(paper[0]['games']), len(paper[1]['games'])])):
            for index in range(2):
                if i < len(paper[index]['games']):
                    game = paper[index]['games'][i]
                    points[pmap[index][game[1]]] += game[0]

            games.append(pos)
            pos += 1
            for i in range(len(history)):
                history[i].append(points[i])

    linechart(title, labels, games, history, db['players'])


def analyze_average_points_per_bar(db):
    title = "Punkte per Kneipe"
    labels = { 'x': "Kneipe", 'y': "Punkte" }

    points = []
    for bar in db['bars']:
        res = 0;
        for paper in bar['paper']:
            for game in paper['games']:
                res += game[0]
        points.append(res)

    barchart(title, labels, list_barnames(db), points)

def analyze_beer_per_bar(db):
    title = "Bierkonsum"
    labels = { 'x': "Kneipe", 'y': "Biermenge" }

    beer = []
    for bar in db['bars']:
        beer.append(bar['beer'])
    beer.append(sum(beer))
    names = list_barnames(db)
    names.append("Gesamt")

    barchart(title, labels, names, beer)

def analyze_games_per_bar(db):
    title = "Spiele per Kneipe"
    labels = { 'x': "Kneipe", 'y': "Spiele" }

    games = []
    for bar in db['bars']:
        num = 0
        for paper in bar['paper']:
            num += len(paper['games'])
        games.append(num)

    games.append(sum(games))
    names = list_barnames(db)
    names.append("Gesamt")
    barchart(title, labels, names, games)

def analyze_games_per_player(db):
    title1 = "Spiele Insgesamt pro Person"
    title2 = "Spiele Gespielt pro Person"
    title3 = "Spieleraktivität"
    labels = { 'x': "Spieler", 'y': "Spiele"}

    games = []
    played = []
    rate = []

    for p in db['players']:
        games.append(0)
        played.append(0)

    for bar in db['bars']:
        for paper in bar['paper']:
            for player in paper['players']:
                games[player] += len(paper['games'])

            pmap = paper['players']
            for game in paper['games']:
                played[pmap[game[1]]] += 1

    for i in range(len(games)):
        tmp = played[i] / games[i]
        rate.append(round(tmp * 100, 1))

    barchart(title1, labels, db['players'], games)
    barchart(title2, labels, db['players'], played)
    barchart(title3, labels, db['players'], rate)



def main(args):
    print("Kneipenskat 3000 - Ergebnis\n")

    print("Lese Resultate -> {}...".format(args.file))
    with open(args.file, "r", encoding='utf-8') as f:
        db = json.loads(f.read())

    # analyze_beer_per_bar(db)
    # analyze_games_per_bar(db)
    # analyze_average_points_per_bar(db)

    # analyze_games_per_player(db)
    analyze_point_tracking(db)
    # analyze_overall_points(db)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file", default="", help="data base file")
    args = p.parse_args()
    main(args)
