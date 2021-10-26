### Almost Yahtzee...

...or not really Yahtzee, just a variation of the game. I've learned it from my girlfriend, there are some notable differences, though the idea stays pretty much the same.

I know the question of optimal strategy for Yahtzee is basically solved, and it should be straightforward to just adapt that approach to this variation of the game. Nevertheless, I've decided to do it completely on my own. 

I'm not sure how close it is to the actual optimal strategy (since the scoring is different than in Yahtzee), or even if the computer is any better than me (since the results are too volatile to judge them based on a less than a zillion of tries).

- *score.py* contains all the necessary routines to score a dice roll;

- Using functions from *generate_moves.py*, for every possible 5-roll you can provide expected value of every figure/declaration, based on an actual zillion of tries. Additionally, it scores those values based on rarity and also provides the optimal move (i.e. which dice to keep before the next throw) for every figure/declaration;

	- *moves.json* contains those results for 20 000 tries.

- Functions from *plan_moves.py* can be used to either choose the best move for every roll, or to order CPU to play the whole game (and tell us his final score).