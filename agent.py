import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction
from model import Linear_QNet, QTrainer
from plot import plot
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(12, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):

        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
     
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # ball location 
            game.ball.left < game.robot1.left,  # ball left
            game.ball.left > game.robot1.left,  # ball right
            game.ball.top < game.robot1.top,  # ball up
            game.ball.top > game.robot1.top,  # ball down

            #Right_Goal_post_location
            game.right_goalpost.top < game.robot1.top, # goal post down
            game.right_goalpost.top > game.robot1.top, #goal post up
            1,                                           #goal post right
            0,                                           #goal post left
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
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
    plot_score1 = []
    plot_score2 = []
    plot_mean_score1=[]
    total_score1 = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score1, score2 = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score1 > record:
                record = score1
                agent.model.save()

            print('Game', agent.n_games, 'Score', score1, 'Record:', record)

            plot_score1.append(score1)
            total_score1 += score1
            plot_score2.append(score2)
            mean_score = total_score1 / agent.n_games
            plot_mean_score1.append(mean_score)
            plot(plot_score1, plot_score2 ,plot_mean_score1)


if __name__ == '__main__':
    train()