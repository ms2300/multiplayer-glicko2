# Glicko
# python 3.4.3
import math
from glicko_classes import *

# Background information - https://en.wikipedia.org/wiki/Glicko_rating_system
# Based on this equation - http://www.glicko.net/glicko/glicko2.pdf

_MAXSIZE = 186
_MAXMULTI = .272
_MULTISLOPE = .00391
_WIN = 1.0
_LOSS = 0
_CATCH = .5
_INITRAT = 1500.0
_INITCONF = 35.0
_INITVOL = .06
_VOL = .2
_CONV = 173.7178
_EPS = 0.001


def findSigma(mu, phi, sigma, change, variance):
    alpha = math.log(sigma ** 2)
    counterx = 0

    def f(x):
        tmp = phi ** 2 + variance + math.exp(x)
        a = math.exp(x) * (change ** 2 - tmp) / (2 * tmp ** 2)
        b = (x - alpha) / (_VOL ** 2)
        return a - b

    a = alpha
    if change ** 2 > phi ** 2 + variance:
        b = math.log(change ** 2 - phi ** 2 - variance)
    else:
        k = 1
        while f(alpha - k * _VOL) < 0:
            k += 1
        b = alpha - k * _VOL
    fa, fb = f(a), f(b)
    while abs(b - a) > _EPS:
        c = a + (a - b) * fa / (fb - fa)
        fc = f(c)
        if fc * fb < 0:
            a, fa = b, fb
        else:
            fa /= 2
        b, fb = c, fc
    return math.e ** (a / 2)


def calculateGlicko(players):
    N = len(players)
    if N > _MAXSIZE:
        multi = _MAXMULTI
    else:
        multi = _WIN - _MULTISLOPE * N
    for i in players:
        mu = (i.rating - _INITRAT) / _CONV
        phi = i.confidence / _CONV
        sigma = i.volatility
        variance_inv = 0
        difference = 0
        for j in players:
            if i is not j:
                oppMu = (j.rating - _INITRAT) / _CONV
                oppPhi = j.confidence / _CONV
                if i.place > j.place:
                    S = _LOSS
                elif i.place < j.place:
                    S = _WIN
                else:
                    S = _CATCH
                weighted = 1 / math.sqrt(1 + 3 * oppPhi ** 2 / math.pi ** 2)
                weighted = weighted * multi
                expected_score = 1 / (1 + math.exp(-weighted * (mu - oppMu)))
                variance_inv += weighted ** 2 * expected_score * \
                    (1 - expected_score)
                difference += weighted * (S - expected_score)
        if variance_inv != 0:
            variance = 1 / variance_inv
            change = variance * difference
            newSigma = findSigma(mu, phi, sigma, change, variance)
            phiAst = math.sqrt(phi ** 2 + newSigma ** 2)
            newPhi = 1 / math.sqrt(1 / phiAst ** 2 + 1 / variance)
            newMu = mu + newPhi ** 2 * difference
            i.rating = newMu * _CONV + _INITRAT
            i.confidence = newPhi * _CONV
            i.volatility = newSigma
