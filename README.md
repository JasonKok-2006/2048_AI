This is an AI that learns to play the game 2048.

The agent.py file is the file that has to be executed in order for it to work.
This works by working with the model.py and game_2048_environment.py files.
The agent runs a set amount of random games collecting training data, trying to
maximise the reward. After the set amount of games have been completed, the model
predicts the best move resulting in reinforcment allowing the model to progress further into
the game.

The plotter_helper.py file contains all the parameters for the matplotlib graph. This allows
the AI to display the progress. There are three lines, highest tile value to see how far the AI 
has managed to get to before game over. The average score (all games) line shows the mean score for 
all the games and the average score (last 10 games) shows the average score of the previous 10 games.
There is a seperate line for the previous 10 game average for clarity, allowing for visual feedback
proving that the modle does indeed learn the game.