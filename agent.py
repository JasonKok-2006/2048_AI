import torch
import random
import numpy as np
from collections import deque
from game_2048_environmemt import Game

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness 
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = None
        self.trainer = None

    def get_state(self, game):
        pass

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
        final_move = None #TODO

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
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

            print("Game: ", agent.n_games, "Score: ", score, "Record: ", record)