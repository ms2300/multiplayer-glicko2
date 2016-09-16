# Copyright (c) 2016 by Matt Sewall.
# All rights reserved.


class GlickoPlayer:
    def __init__(self, name, school, place, rating, confidence, volatility):
        self.name = name
        self.school = school
        self.place = place
        self.rating = rating
        self.confidence = confidence
        self.volatility = volatility

    def __eq__(self, other):
        return self.name == other.name and \
               self.school == other.school

    def __hash__(self):
        return hash((self.name, self.school))


# Used as a class for example.py, and is not relevant to the core algorithm


class Player:
    def __init__(self, name, school):
        self.name = name
        self.school = school

    def __eq__(self, other):
        return self.name == other.name and \
               self.school == other.school

    def __hash__(self):
        return hash((self.name, self.school))

    def __repr__(self):
        return self.name


class RatingPeriod:
    competitors = []

    def addCompetitor(self, name, school, place, rating, confidence,
                      volatility):
        competitor = GlickoPlayer(name, school, place, rating, confidence,
                                  volatility)
        self.competitors.append(competitor)
