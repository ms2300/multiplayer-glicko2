#Introduction

From [Wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system),

The Elo rating system is a method for calculating the relative skill levels of players in competitor-versus-competitor games such as chess. It is named after its creator Arpad Elo, a Hungarian-born American physics professor.

The Elo system was originally invented as an improved chess rating system but is also used as a rating system for multiplayer competition in a number of video games, association football, gridiron football, basketball, Major League Baseball, Scrabble, snooker and other games.

The difference in the ratings between two players serves as a predictor of the outcome of a match. Two players with equal ratings who play against each other are expected to score an equal number of wins. A player whose rating is 100 points greater than their opponent's is expected to score 64%; if the difference is 200 points, then the expected score for the stronger player is 76%.

A player's Elo rating is represented by a number which increases or decreases depending on the outcome of games between rated players. After every game, the winning player takes points from the losing one. The difference between the ratings of the winner and loser determines the total number of points gained or lost after a game. In a series of games between a high-rated player and a low-rated player, the high-rated player is expected to score more wins. If the high-rated player wins, then only a few rating points will be taken from the low-rated player. However, if the lower rated player scores an upset win, many rating points will be transferred. The lower rated player will also gain a few points from the higher rated player in the event of a draw. This means that this rating system is self-correcting. A player whose rating is too low should, in the long run, do better than the rating system predicts, and thus gain rating points until the rating reflects their true playing strength.

<hr>

My exact algorithm is based off the ideas laid out [here](http://elo-norsak.rhcloud.com/index.php)


### The Specifics

This specific variation of the elo ranking system is designed for large multiplayer competitions with the number of competitors ideally being between 20 and 190 runners. This program was initially wrote with the intention of ranking cross country meets and therefore had to be both flexible on size of competition and unpredictability of competitors. While there have been multiplayer versions of elo written before (and even one based off the same source), to my knowledge none have been wrote that are suited for something as large as cross country.


### Deviations from Original Head-to-Head Algorithm

- Competition wide k value now scales linearly downward as the size of the competition grows

- About the top 5% of overall competitors within a system receive lower k values to stabilize ratings on the edge of the bell curve and reduce the potential for elo deflation.

- Expected score algorithm changed slightly to make an elo difference of 400 points have an expected score of .25 instead of .0909 and .75 instead of .909 respectively.

- Make the floor of an elo ranking be zero


### Example

I've included and example.py file and a small json file containing 5 high school cross country meets from 2005 in Oregon. To run the example and see the elo changes that these meets produce run ->
```
python example.py smallish.json
```
Make sure you have django smart_str and smart_unicode installed


### Large Scale

I have used this algorithm to effectively rank almost every single high school cross country from the last decade. Running this algorithm with 1,075,214 boy runners, 871,502 girl runners and 197,571 competitions, I produced a mean elo of 1498 for girls and a mean elo of 1499 for boys respectively. In addition, the results seemed to map the desired bell curve pretty darn well.

![alt tag](https://github.com/ms2300/multiplayer-elo/blob/master/img/boysEloHistogram.png)
<hr>
![alt tag](https://github.com/ms2300/multiplayer-elo/blob/master/img/girlsEloHistogram.png)


Finally, this program graphed history / elo over time for every athlete that I had data on. For instance my graph from time running in high school is shown below.

![alt tag](https://github.com/ms2300/multiplayer-elo/blob/master/img/mattSewallElo.png)
