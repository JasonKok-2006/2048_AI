import torch
import random
import numpy as np
from collections import deque
from game_2048_environmemt import Game
from model import Linear_QNet, QTrainer
from plotter_helper import plot

MAX_MEMORY = 10000
BATCH_SIZE = 500
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness 
        self.gamma = 0.9 #discount rate (keep samller then 1)
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(16, 256, 4)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

    def get_state(self, board): 
        # Flatten the board for input
        flat_board = np.array(board).flatten()
        flat_board = flat_board / max(flat_board.max(), 1)
        return flat_board

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
        self.epsilon = max(2, 200 - self.n_games)
        final_move = [0, 0, 0, 0]

        if random.randint(0, 300) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    
def train():
    plot_last10_avaerage_scores = []
    plot_mean_scores = []
    plot_highest = []
    last10_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_score = 0
    last10_scores_average = 0
    record = 0
    agent = Agent()
    game = Game()
    #game.start_game()
    while True:
        #get the board
        board = game.board

        #get old state
        old_state = agent.get_state(board)

        #get move
        final_move = agent.get_action(old_state)

        #get the board
        board = game.board

        #performs move and gets new state
        move = final_move.index(1)
        reward, done, score = game.game_step(move)
        new_state = agent.get_state(board)

        #train the short memory
        agent.train_short_memory(old_state, final_move, reward, new_state, done)

        #remember
        agent.remember(old_state, final_move, reward, new_state, done)

        if done:
            #train long memory, plot result
            game.reset()
            non_zero = 0
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print("Game: ", agent.n_games, "Score: ", score, "Record: ", record)

            for i in range(0, 9):
                last10_scores[i] = last10_scores[i+1]
            last10_scores[9] = score

            for i in range(0, 10):
                if last10_scores[i] > 0:
                    last10_scores_average += last10_scores[i]
                    non_zero += 1

            last10_scores_average = int(last10_scores_average / non_zero)

            plot_last10_avaerage_scores.append(last10_scores_average)
            total_score += score 
            mean_score = int(total_score / agent.n_games)
            plot_mean_scores.append(mean_score)

            row_max = []
            for row in board:
                row_max.append(max(row))
            highest_tile = max(row_max)

            plot_highest.append(highest_tile)
            plot(plot_last10_avaerage_scores, plot_mean_scores, plot_highest)
            score = 0

if __name__ == "__main__":
    train()