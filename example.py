# Glicko
# python 3.4.3
import math
import csv
import json
import os
import shutil
from sys import argv
from datetime import datetime
from django.utils.encoding import smart_str, smart_unicode
from operator import itemgetter
from glicko import *
from glicko_classes import *


# Ratings dictionaries contain athletes keyed to an elo value
# Entries dictionaries contain athletes keyed to history of their results

ratings_boys = {}
ratings_girls = {}
entries_boys = {}
entries_girls = {}
_INITRAT = 1500.0
_INITCONF = 35.0
_INITVOL = .06


def do_glicko(data, meetName, meetDate, gender):
    if gender == "female":
        ratings = ratings_girls
        entries = entries_girls
    elif gender == "male":
        ratings = ratings_boys
        entries = entries_boys

    # Add players to competition and calculate ratings

    meet = RatingPeriod()
    meet.competitors = []
    for dat in data:
        name = dat[0]
        school = dat[2]
        place = int(dat[1])
        player = Player(name, school)
        if player in ratings:
            rating = float(ratings.get(player)[0])
            confidence = float(ratings.get(player)[1])
            vol = float(ratings.get(player)[2])
            meet.addCompetitor(name, school, place, rating, confidence, vol)
        else:
            # Initial ratings if a player hasn't competed before
            meet.addCompetitor(name, school, place, _INITRAT, _INITCONF,
                               _INITVOL)
    if len(meet.competitors) > 1:
        calculateGlicko(meet.competitors)

        # Take results of competition and append data

        for runner in meet.competitors:
            ath = Player(runner.name, runner.school)
            ratings[ath] = [runner.rating, runner.confidence,
                            runner.volatility]
            if ath in entries:
                res_list = entries.get(ath)
                res_list.append([meetName, meetDate,
                                runner.rating, runner.confidence])
                entries[ath] = res_list
            else:
                entries[ath] = [[meetName, meetDate,
                                runner.rating, runner.confidence]]


def align_data(filename):
    filex = open(filename)
    sort = []
    for json_string in filex:
        parsed = json.loads(json_string)
        results = parsed["results"]
        kill = False
        locs = parsed["meetLocation"]
        a_date = parsed["meetDate"]
        exact_date = datetime.strptime(a_date[0], "%A, %B %d, %Y")
        for loc in locs:
            if loc == u'Collegiate' or loc == u'MS':
                kill = True
        for result in results:
            if result.keys() == [u'maleResults'] or [u'femaleResults']:
                static = result.values()
                events = static[0]
                for event in events:
                    data = []
                    data.append(exact_date)
                    data.append(parsed['meetName'])
                    if result.keys() == [u'maleResults']:
                        data.append("male")
                    elif result.keys() == [u'femaleResults']:
                        data.append("female")
                    places = []
                    details = event[u'eventDetails']
                    for detail in details:
                        killx = False
                        ath_detail_List = []
                        if detail[u'resultName'] == " " or \
                                detail[u'resultName'] == u' ' or \
                                detail[u'resultName'] == []:
                            killx = True
                        ath_detail_List.append(
                                        smart_str(detail[u'resultName']))
                        if detail[u'resultPlace'] == " " or \
                                detail[u'resultPlace'] == u' ':
                            killx = True
                        else:
                            ath_detail_List.append(detail[u'resultPlace'])
                        ath_detail_List.append(
                                        smart_str(detail[u'resultSchool']))
                        if killx is False:
                            places.append(ath_detail_List)
                    data.append(places)
                    if kill is False:
                        sort.append(data)
    sortx = sorted(sort, key=itemgetter(0))
    return sortx


def write_ath(entries):
    if entries == entries_boys:
        path = "./meetsGlicko/boys"
    elif entries == entries_girls:
        path = "./meetsGlicko/girls"
    if not os.path.exists("./meetsGlicko/"):
        os.mkdir("./meetsGlicko/")
    if not os.path.exists(path):
        os.mkdir(path + "/")
    for ath in entries:
        school_path = os.path.join(path, ath.school)
        ath_path = os.path.join(school_path, ath.name + ".csv")
        filename = "%s.csv" % ath.name
        with open((filename), "w") as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(entries[ath])
        if os.path.exists(school_path):
            shutil.move(filename, ath_path)
        else:
            os.mkdir(school_path)
            shutil.move(filename, ath_path)


def write_rating(ratings, gender):
    if gender == "male":
        name = "athlete_glicko_boys.csv"
    elif gender == "female":
        name = "athlete_glicko_girls.csv"
    with open((name), "w") as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(ratings)


def main():
    events = align_data(argv[1])
    for event in events:
        if len(event) == 4:
            name = smart_str(event[1][0])
            date = event[0]
            gender = event[2]
            do_glicko(event[3], name, date, gender)
    sorted_boys = sorted(ratings_boys.items(), key=itemgetter(1))
    sorted_girls = sorted(ratings_girls.items(), key=itemgetter(1))
    write_rating(sorted_boys, "male")
    write_rating(sorted_girls, "female")
    write_ath(entries_girls)
    write_ath(entries_boys)

if __name__ == '__main__':
    main()
