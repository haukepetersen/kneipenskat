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

players = []
bars = []


def readline(promt):
    line = ""
    while line == "":
        line = input(promt)
    return line

def readtime():
    while True:
        line = readline("-> ")
        m = re.match("^(\d\d):(\d\d)$", line)
        if m and int(m.group(1)) < 24 and int(m.group(2)) < 60:
            return line

def readint(min, max):
    try:
        val = int(readline("-> "))
        if val >= min and val <= max:
            return val
        else:
            readint(min, max)
    except ValueError:
        return readint(min, max)

def readfloat():
    try:
        return float(readline("-> "))
    except ValueError:
        return readfloat()

def time2str(time):
    return time

def chunk(str):
    print(str, end='')


def in_confirm():
    return readline("Tippen Sie 'j' um zu bestätigen -> ").lower() == 'j'

def in_players():
    players.clear()
    name = "xxx"
    while name != "":
        name = input("-> ")
        if name != "":
            players.append(name)

    print("{} Spieler wurden eingegeben".format(len(players)))

def list_players():
    for i, p in enumerate(players):
        print("[{:2}] {}".format(i, p))


def select_player():
    list_players()
    selection = ""
    while not selection.isnumeric() or int(selection) >= len(players):
        selection = readline("-> ")
        if not selection.isnumeric():
            selection = ""

    return int(selection)

def name(id):
    return players[id]

def list_paper(players, games):
    paper = [0, 0, 0]
    for i in range(3):
        print(name(players[i]))
    print("{:>10} | {:>10} | {:>10} | {:>10}".format(name(players[0]),
                                                     name(players[1]),
                                                     name(players[2]), "Spiel"))
    print("=================================================")
    for i, game in enumerate(games):
        for p in range(3):
            if p == game[1]:
                paper[p] += game[0]
                chu = "{:>10} | ".format(paper[p])
            else:
                chu = "{:>10} | ".format("-")
            chunk(chu)

        print("{:>10}".format(game[0]))
        if ((i + 1) % 3) == 0:
            print("-------------------------------------------------")

    print("{:>10} | {:>10} | {:>10} | {:>10}".format(paper[0], paper[1], paper[2], "-"))
    print("=================================================")


def in_bar():
    conf = False
    bar = {"paper": []}
    while not conf:
        print("Name der Kneipe:")
        bar['name'] = readline("-> ")
        print("Uhrzeit bei Ankunft:")
        bar['time'] = readtime()
        print("Biermenge:")
        bar['beer'] = readfloat()
        print("Folgende Daten wurden genannt:")
        print('Name der Kneipe: "{}"'.format(bar['name']))
        print('Uhrzeit bei Ankunft: {}'.format(time2str(bar['time'])))
        print('Konsumiertes Bier: {}l'.format(bar['beer']))
        print("Sind diese Daten korrekt?")
        conf = in_confirm()

    bar['paper'].append({})
    bar['paper'].append({})
    for paper in range(2):
        game = bar['paper'][paper]
        game['players'] = []
        game['games'] = []
        conf = False
        print("--- Zettel Nr. {} ---".format(paper + 1))
        while not conf:
            game['players'].clear()
            for p in range(3):
                print("Spieler {}".format(p + 1))
                game['players'].append(select_player())
            print("Spielrunde:")
            for p in range(3):
                print("Spieler {}: {}".format(p + 1, name(game['players'][p])))
            print("Sind die Angaben korrekt?")
            conf = in_confirm()

        conf = False
        while not conf:
            game['games'].clear()

            more = True
            while more:
                for i in range(3):
                    print("Spiel:")
                    points = readint(-9999, 9999)
                    print("Gespielt:")
                    who = readint(1, 3)
                    game['games'].append((points, (who - 1)))
                print("Neue Runde?")
                more = readline("'j' für Ja -> ").lower() == 'j'

            print("Ergebnisse:")
            list_paper(game['players'], game['games'])
            print("Stimmen diese Zahlen?")
            conf = in_confirm()

    print("Kneipe fertig gelesen")
    bars.append(bar)





def main():
    print("Kneipenskat 3000 - Ergebniserfassung\n")

    conf = False
    while not conf:
        print("--- Erfassung der Mitspieler ---")
        print("Bitte geben Sie die Namen der Mitspieler ein:")
        in_players()
        print("Folgende Spieler waren dabei:")
        list_players()
        print("Ist die Eingabe Korrekt?")
        conf = in_confirm()
        print("")

#    pp = [2, 0, 1]
#    games = [(30, 2), (18, 0), (-38, 1), (-80, 2), (-36, 1), (42, 0)]
#    list_paper(pp, games)

    cont = True
    while cont:
        print("--- Erfassung Kneip Nr. {} ---".format(len(bars) + 1))
        print("Möchten Sie fortfahren?")
        if in_confirm():
            in_bar()
        else:
            cont = False

    print("\n--- Resultate ---")


    # finally: save file
    with open("foo.db", "w") as f:
        f.write(json.dumps({'players': players, 'bars': bars}))

if __name__ == "__main__":
    main()
