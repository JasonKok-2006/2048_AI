import torch
import random
import numpy as np
from collections import deque
from game_2048_environmemt import Game
from model import Linear_QNet, QTrainer
from plotter_helper import plot

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness 
        self.gamma = 0.9 #discount rate (keep samller then 1)
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(2, 256, 4)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

    def get_state(self, game):
        board = game.board
        high_tile = max(board)

        #split the grid into 4 2x2 squares (keep track of the hoghest value)
        for i in range(0, 4):
            for j in range(0, 4):
                if board[i][j] == high_tile:
                    high_tile_space_value = (4*i) + j
                    break

        if high_tile_space_value in (0, 1, 4, 5):
            square = 1
        elif high_tile_space_value in (2, 3, 6, 7):
            square = 2
        elif high_tile_space_value in (8, 9, 12, 13):
            square = 3
        else:
            square = 4
        
        #[1, 0, 0, 0] -> move left
        #[0, 1, 0, 0] -> move right
        #[0, 0, 1, 0] -> move up
        #[0, 0, 0, 1] -> move down

        #depending on where the high tile is, we make the move bring the tile closer to the corner.
        #Random is being used here so if the move is actually invalid, the model will eventually make the valid move.
        #chances are that this needs to be tweaked, we'll see.

        if square == 1:
            if high_tile_space_value == 1:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [1, 0, 0, 0]
                else:
                    action = [0, 0, 1, 0]
            elif high_tile_space_value == 4:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [0, 0, 1, 0]
                else:
                    action = [1, 0, 0, 0]
            else:
                random_action = random.randint(0, 100)
                if random_action > 50:
                    action = [0, 0, 1, 0]
                else:
                    action = [1, 0, 0, 0]
        elif square == 2:
            if high_tile_space_value == 2:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [0, 1, 0, 0]
                else:
                    action = [0, 0, 1, 0]
            elif high_tile_space_value == 7:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [0, 0, 1, 0]
                else:
                    action = [0, 1, 0, 0]
            else:
                random_action = random.randint(0, 100)
                if random_action > 50:
                    action = [0, 0, 1, 0]
                else:
                    action = [0, 1, 0, 0]
        if square == 3:
            if high_tile_space_value == 8:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [0, 0, 0, 1]
                else:
                    action = [1, 0, 0, 0]
            elif high_tile_space_value == 13:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [1, 0, 0, 0]
                else:
                    action = [0, 0, 0, 1]
            else:
                random_action = random.randint(0, 100)
                if random_action > 50:
                    action = [0, 0, 0, 1]
                else:
                    action = [1, 0, 0, 0]
        else:
            if high_tile_space_value == 14:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [0, 1, 0, 0]
                else:
                    action = [0, 0, 0, 1]
            elif high_tile_space_value == 11:
                random_action = random.randint(0, 100)
                if random_action > 20:
                    action = [0, 0, 0, 1]
                else:
                    action = [0, 1, 0, 0]
            else:
                random_action = random.randint(0, 100)
                if random_action > 50:
                    action = [0, 0, 0, 1]
                else:
                    action = [0, 1, 0, 0]

        return action

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)        

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration/explotation
        self.epsilon = 80 - self.n_games
        final_move = [1, 0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores =[]
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:
        #get old state
        old_state = agent.get_state(game)

        #get move
        final_move = agent.get_action(old_state)

        #performs move and gets new state
        reward, done, score = game.game_step(final_move)
        new_state = agent.get_state(game)

        #train the short memory
        agent.train_short_memory(old_state, final_move, reward, new_state, done)

        #remember
        agent.remember(old_state, final_move, reward, new_state, done)

        if done:
            #train long memory, plot result
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print("Game: ", agent.n_games, "Score: ", score, "Record: ", record)

            plot_scores.append(score)
            total_score += score 
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

train()