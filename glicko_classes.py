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
    players = []

    def addPlayer(self, name, school, place, rating, confidence, volatility):
        player = GlickoPlayer(name, school, place, rating, confidence,
                              volatility)
        self.players.append(player)
