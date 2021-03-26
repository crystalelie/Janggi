# Janggi

JanggiGame is a Korean board game, which is similar to Chess. Each piece has specific rules dictating where they can move. The starting
player will always be Blue. Each player takes turns moving a piece. If the move is invalid, either resulting in the player's General
being in check, or the move is not valid in terms of the piece's rules, it will return False and will force the player to attempt another,
valid move. When a General is in check, the player is required to move them out of check on their next turn. If they try to move a piece in a way
that does not take their General out of check, it will return False and force the player to attempt another, valid move. If the player has no valid 
moves to get their General out of check, this results in a checkmate and the other player wins. 

Each of the 7 differing game pieces (Chariot, Horse, Elephant, Guard, General, Cannon and Soldier) are programmed to their own rule set based on the rules
of how they are able to move. If they make a move that is invalid based on their rule set, the move will return False and they will have to attempt a 
different move.

After verifying that the move is valid per the pieces's rule set, the game will check to make sure that the player is not making a move that would put their 
General in check. If it does not put their General in check, the game will make the move, and then check to see if the other player's General is in check.
It is programmed to create a dictionary of valid moves of the player's General and it will create a dictionary of all of the valid moves of the opposing player's
pieces. If the General's current position is in the enemy's dictionary of valid moves, then it will indicate that the player is in check and will force them to 
make a move on their next turn to move out of check.

Players are able to play the game in the console of PyCharm.
