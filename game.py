import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set the dimensions of the playing field
WIDTH = 800
HEIGHT = 500
# Set the dimensions of the ball and robots
BALL_RADIUS = 15
ROBOT_RADIUS = 30

# Set the maximum speed of the robots
MAX_SPEED = 40


# Set the duration of the game
GAME_DURATION = 20  # seconds

# Set the scoring threshold
SCORE_THRESHOLD = 3


class SnakeGameAI:

    def __init__(self, w=800, h=500):
        self.w = w
        self.h = h
        # init display
        pygame.display.set_caption("Soccer Simulator")
        self.screen = pygame.display.set_mode((self.w, self.h))

        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.playing_field = pygame.Rect(0, 0, WIDTH, HEIGHT)

        # Define the goalposts
        self.left_goalpost = pygame.Rect(0, HEIGHT/2, BALL_RADIUS, 150)
        self.right_goalpost = pygame.Rect(WIDTH - BALL_RADIUS, HEIGHT/2, BALL_RADIUS, 150)

        # Define the robots
        self.robot1 = pygame.Rect(WIDTH/4, HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)
        # TODO: self.robot2 = pygame.Rect(WIDTH/4, HEIGHT-HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)
        self.robot3 = pygame.Rect(WIDTH-WIDTH/4, HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)
        # TODO: self.robot4 = pygame.Rect(WIDTH-WIDTH/4, HEIGHT-HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)
    
        # Define the ball
        self.ball = pygame.Rect(WIDTH/2, HEIGHT/2, BALL_RADIUS, BALL_RADIUS)
    
        # Set the initial velocity of the ball
        self.ball_speed_x = 3
        self.ball_speed_y = 3
    
        # Set the initial score
        self.score1 = 0
        self.score2 = 0
    
        # Set the start time of the game
        self.start_time = pygame.time.get_ticks()
        self.frame_iteration = 0
        self.reward=0


      


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        
        
        # 3. check if game over

        game_over = False
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed_time >= GAME_DURATION:
            game_over = True
            
            return self.reward, game_over, self.score1,self.score2



            

        if self.ball.colliderect(self.robot1):


            print(self.reward)

        if self.ball.colliderect(self.left_goalpost):
            self.score2 += 1
            self.ball.center = (WIDTH/2, HEIGHT/2)
            self.reward += 100
            self.ball_speed_x = 0
            self.ball_speed_y = 0
            self.ball.move_ip(0, 0)
            print('y')
        if self.ball.colliderect(self.right_goalpost):
            self.score1 += 1
            self.ball.center = (WIDTH/2, HEIGHT/2)
            self.ball_speed_x=0
            self.ball_speed_y=0
            self.ball.move_ip(0, 0)
            self.reward -= 50
            print('y')

        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(MAX_SPEED)
        # 6. return game over and score
        return self.reward, game_over, self.score1, self.score2

    # Check for collisions with the playing field
    def is_collision_pf(self):
       
        if not self.playing_field.contains(self.robot1):
            self.robot1.clamp_ip(self.playing_field)
            print(1)
            return True
        if not self.playing_field.contains(self.robot3):
            self.robot3.clamp_ip(self.playing_field)
        if not self.playing_field.contains(self.ball):
            self.ball.clamp_ip(self.playing_field)
            self.ball_speed_x = -self.ball_speed_x
            self.ball_speed_y = -self.ball_speed_y
        return False
    
    # Check for collisions with the ball        
    def is_collision_ball(self):
        if self.ball.colliderect(self.robot1):
            if self.direction == Direction.RIGHT:
                self.ball_speed_x = 2*MAX_SPEED
                self.ball_speed_y = 0
            elif self.direction == Direction.LEFT:
                self.ball_speed_x = -2*MAX_SPEED
                self.ball_speed_y = 0
                
            elif self.direction == Direction.DOWN:
                self.ball_speed_x = 0
                self.ball_speed_y = 2*MAX_SPEED
                
            elif self.direction == Direction.UP:
                self.ball_speed_x = -2*MAX_SPEED
                self.ball_speed_y = 0
            return True
        if self.ball.colliderect(self.robot3): 
            self.ball_speed_x = random.uniform(-2*MAX_SPEED, 2*MAX_SPEED)
            self.ball_speed_y = random.uniform(-2*MAX_SPEED, 2*MAX_SPEED)
        self.ball.move_ip(self.ball_speed_x, self.ball_speed_y)
        return False
    
    # Check for collisions with the goalposts
    def is_collision_goal(self):
        if self.ball.colliderect(self.left_goalpost):
            self.score2 += 1
            self.ball.center = (WIDTH/2, HEIGHT/2)
            return 0
        if self.ball.colliderect(self.right_goalpost):
            self.score1 += 1
            self.ball.center = (WIDTH/2, HEIGHT/2)
            return 1
        
        


    def _update_ui(self):
        self.screen.fill(BLACK)

    # Draw the playing field
        pygame.draw.rect(self.screen, GREEN, self.playing_field)

            # Draw the goalposts
        pygame.draw.rect(self.screen, WHITE, self.left_goalpost)
        pygame.draw.rect(self.screen, WHITE, self.right_goalpost)

        # Draw the robots and the ball
        pygame.draw.rect(self.screen, RED, self.robot1)
        #pygame.draw.rect(self.screen, BLUE, robot2)
        pygame.draw.rect(self.screen, WHITE, self.robot3)
        #pygame.draw.rect(self.screen, BLACK, robot4)
        pygame.draw.circle(self.screen, WHITE, self.ball.center, BALL_RADIUS)

        # Draw the scores
        text1 = font.render(str(self.score1), True, WHITE)
        text2 = font.render(str(self.score2), True, WHITE)
        self.screen.blit(text1, (WIDTH/4, 10))
        self.screen.blit(text2, (3*WIDTH/4, 10))

        # Update the display
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left, back]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        elif np.array_equal(action, [0, 0, 1, 0]):
            next_idx = (idx -1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d
        elif np.array_equal(action, [0, 0, 0, 1]):
            next_idx = (idx -2) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        if self.direction == Direction.RIGHT:
            self.robot1.move_ip(MAX_SPEED,0)
        elif self.direction == Direction.LEFT:
            self.robot1.move_ip(-MAX_SPEED,0)
        elif self.direction == Direction.DOWN:
            self.robot1.move_ip(0,MAX_SPEED)
        elif self.direction == Direction.UP:
            self.robot1.move_ip(0,-MAX_SPEED)
        self.robot3.move_ip(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))

        if self.ball.colliderect(self.robot1):

            if self.direction == Direction.RIGHT:
                self.ball_speed_x = 0.5 * MAX_SPEED
                self.ball_speed_y = 0
            elif self.direction == Direction.LEFT:
                self.ball_speed_x = -0.5 * MAX_SPEED
                self.ball_speed_y = 0

            elif self.direction == Direction.DOWN:
                self.ball_speed_x = 0
                self.ball_speed_y = 0.4 * MAX_SPEED

            elif self.direction == Direction.UP:
                self.ball_speed_x = -0.4* MAX_SPEED
                self.ball_speed_y = 0

        if self.ball.colliderect(self.robot3):

            self.ball_speed_x = random.uniform(-0.5 * MAX_SPEED, 0.4 * MAX_SPEED)
            self.ball_speed_y = random.uniform(-0.5 * MAX_SPEED, 0.3 * MAX_SPEED)
        self.ball.move_ip(self.ball_speed_x, self.ball_speed_y)


        if not self.playing_field.contains(self.robot1):
            self.robot1.clamp_ip(self.playing_field)


        if not self.playing_field.contains(self.robot3):
            self.robot3.clamp_ip(self.playing_field)
        if not self.playing_field.contains(self.ball):
            self.ball.clamp_ip(self.playing_field)
            self.ball_speed_x = -self.ball_speed_x
            self.ball_speed_y = -self.ball_speed_y







        