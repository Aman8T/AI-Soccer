import pygame
import random

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set the dimensions of the playing field
WIDTH = 1500
HEIGHT = 1000

# Set the dimensions of the ball and robots
BALL_RADIUS = 15
ROBOT_RADIUS = 30

# Set the maximum speed of the robots
MAX_SPEED = 2

# Set the duration of the game
GAME_DURATION = 180  # seconds

# Set the scoring threshold
SCORE_THRESHOLD = 3

# Initialize pygame
pygame.init()

# Set the font for the score display
font = pygame.font.SysFont(None, 48)

# Set the title of the game window
pygame.display.set_caption("Soccer Simulator")

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define the playing field
playing_field = pygame.Rect(0, 0, WIDTH, HEIGHT)

# Define the goalposts
left_goalpost = pygame.Rect(0, HEIGHT/2, BALL_RADIUS, 150)
right_goalpost = pygame.Rect(WIDTH - BALL_RADIUS, HEIGHT/2, BALL_RADIUS, 150)

# Define the robots
robot1 = pygame.Rect(WIDTH/4, HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)
robot2 = pygame.Rect(WIDTH/4, HEIGHT-HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)
robot3 = pygame.Rect(WIDTH-WIDTH/4, HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)
robot4 = pygame.Rect(WIDTH-WIDTH/4, HEIGHT-HEIGHT/4, 2*ROBOT_RADIUS, 2*ROBOT_RADIUS)

# Define the ball
ball = pygame.Rect(WIDTH/2, HEIGHT/2, BALL_RADIUS, BALL_RADIUS)

# Set the initial velocity of the ball
ball_speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)

# Set the initial score
score1 = 0
score2 = 0

# Set the start time of the game
start_time = pygame.time.get_ticks()

# Start the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the robots randomly
    robot1.move_ip(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
    robot2.move_ip(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
    robot3.move_ip(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
    robot4.move_ip(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))

    # Check for collisions with the playing field
    if not playing_field.contains(robot1):
        robot1.clamp_ip(playing_field)
    if not playing_field.contains(robot2):
        robot2.clamp_ip(playing_field)
    if not playing_field.contains(robot3):
        robot3.clamp_ip(playing_field)
    if not playing_field.contains(robot4):
        robot4.clamp_ip(playing_field)

    # Check for collisions with the ball
    if ball.colliderect(robot1):
        ball_speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
        ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
    if ball.colliderect(robot2):
        ball_speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
        ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
    if ball.colliderect(robot3):
        ball_speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
        ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
    if ball.colliderect(robot4):
        ball_speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
        ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)

    # Update the position of the ball
    ball.move_ip(ball_speed_x, ball_speed_y)

    # Check for collisions with the playing field
    if not playing_field.contains(ball):
        ball.clamp_ip(playing_field)
        ball_speed_x = -ball_speed_x
        ball_speed_y = -ball_speed_y

    # Check for collisions with the goalposts
    if ball.colliderect(left_goalpost):
        score2 += 1
        ball_speed_x = random.uniform(0, MAX_SPEED)
        ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
        ball.center = (WIDTH/2, HEIGHT/2)
    if ball.colliderect(right_goalpost):
        score1 += 1
        ball_speed_x = random.uniform(-MAX_SPEED, 0)
        ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
        ball.center = (WIDTH/2, HEIGHT/2)

    # Check for end of game
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if elapsed_time >= GAME_DURATION or score1 >= SCORE_THRESHOLD or score2 >= SCORE_THRESHOLD:
        # Display the final score
        text1 = font.render(str(score1), True, WHITE)
        text2 = font.render(str(score2), True, WHITE)
        screen.blit(text1, (WIDTH/4, HEIGHT/2))
        screen.blit(text2, (3*WIDTH/4, HEIGHT/2))
        pygame.display.flip()
        pygame.time.wait(3000)
        # Reset the game state
        robot1.center = (random.uniform(0, WIDTH/2), random.uniform(0, HEIGHT))
        robot2.center = (random.uniform(WIDTH/2, WIDTH), random.uniform(0, HEIGHT))
        robot3.center = (random.uniform(0, WIDTH/2), random.uniform(0, HEIGHT))
        robot4.center = (random.uniform(WIDTH/2, WIDTH), random.uniform(0, HEIGHT))
        ball.center = (WIDTH/2, HEIGHT/2)
        ball_speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
        ball_speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)
        score1 = 0
        score2 = 0
        start_time = pygame.time.get_ticks()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the playing field
    pygame.draw.rect(screen, GREEN, playing_field)

        # Draw the goalposts
    pygame.draw.rect(screen, WHITE, left_goalpost)
    pygame.draw.rect(screen, WHITE, right_goalpost)

    # Draw the robots and the ball
    pygame.draw.rect(screen, RED, robot1)
    pygame.draw.rect(screen, BLUE, robot2)
    pygame.draw.rect(screen, WHITE, robot3)
    pygame.draw.rect(screen, BLACK, robot4)
    pygame.draw.circle(screen, WHITE, ball.center, BALL_RADIUS)

    # Draw the scores
    text1 = font.render(str(score1), True, WHITE)
    text2 = font.render(str(score2), True, WHITE)
    screen.blit(text1, (WIDTH/4, 10))
    screen.blit(text2, (3*WIDTH/4, 10))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()