#Introduction

From [Wikipedia](https://en.wikipedia.org/wiki/Glicko_rating_system),

The Glicko rating system and Glicko-2 rating system are methods for assessing a player's strength in games of skill, such as chess and go. It was invented by Mark Glickman as an improvement of the Elo rating system, and initially intended for the primary use as a chess rating system. Glickman's principal contribution to measurement is "ratings reliability", called RD, for ratings deviation.

Both Glicko and Glicko-2 rating systems are under public domain and found implemented on game servers online (like Lichess, Free Internet Chess Server, Chess.com, Counter Strike: Global Offensive, Guild Wars 2).[1] The formulas used for the systems can be found on the Glicko website.

The RD measures the accuracy of a player's rating, with one RD being equal to one standard deviation. For example, a player with a rating of 1500 and an RD of 50 has a real strength between 1400 and 1600 (two standard deviations from 1500) with 95% confidence. Twice the RD is added and subtracted from their rating to calculate this range. After a game, the amount the rating changes depends on the RD: the change is smaller when the player's RD is low (since their rating is already considered accurate), and also when their opponent's RD is high (since the opponent's true rating is not well known, so little information is being gained). The RD itself decreases after playing a game, but it will increase slowly over time of inactivity.

The Glicko-2 rating system improves upon the Glicko rating system and further introduces the rating volatility σ. A very slightly modified version of the Glicko-2 rating system is implemented by the Australian Chess Federation.

<hr>

My exact algorithm follows [here](http://www.glicko.net/glicko/glicko2.pdf)


### The Specifics

This variation of the Glicko-2 Rating System is designed for large multiplayer games consisting of anywhere between 20 and 190 competitors. This program was designed for ranking individual high school cross country runners based on large amounts of data. As opposed to elo, glicko ratings are much more difficult to control when competitions become quite large (<150 competitors), and therefore the constants such as initial confidence and both system volatility and initial volatility are very open to change as required.


### Deviations from Original Head-to-Head Algorithm

- The weight for each head to head matchup is not only based on opponents phi value but also on the size of the competition the player is competing in

- The epsilon value relating to the sigma optimization function is much larger than recommended in an effort to cut back on amount of iterations at the slight loss of quality

- The initial confidence value is magnitudes lower than recommended due to the fact that if a first time competitor scored highly in a fairly high ranked competition, the algorithm would run wild, the competitor would gain huge amounts of points, and the entire system would slowly spiral out of control.

- The initial volatility and system wide volatility values are magnitudes lower than recommended for the same reason stated above.


### Example

I've included and example.py file and a small json file containing 5 high school cross country meets from 2005 in Oregon. To run the example and see the rating changes that these meets produce run ->
```
python example.py smallish.json
```
Make sure you have django smart_str and smart_unicode installed


### Large Scale Cross County Meets

I have used this algorithm to effectively rank almost every single high school cross country from the last decade. Running this algorithm with x boy runners, y girl runners and z competitions, I produced a mean elo of xxxx for girls and a mean elo of yyyy for boys respectively. In addition, the ratings produced a nicely ordered bell curve just like they theoretically should.

![alt tag](https://github.com/ms2300/multiplayer-glicko2/blob/master/img/boysGlickoHistogram.png)
<hr>
![alt tag](https://github.com/ms2300/multiplayer-glicko2/blob/master/img/girlsGlickoHistogram.png)


Finally, this program graphed history / glicko2 over time for every athlete that I had data on. For instance my graph over time running in high school is shown below.

![alt tag](https://github.com/ms2300/multiplayer-glicko2/blob/master/img/mattSewallGlicko.png)
