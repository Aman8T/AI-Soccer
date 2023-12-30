# AI-Soccer
The playing field is a rectangular shape with a width of 1500 and a height of 1000 units.
The goalposts are located at either end of the rectangular field with a width of 15 units each.
The football is a circle of radius 15 units.
There are a total of 2 robots, 1 is a random agent (playing randomly) and 1 is our RL Agent. Each robot is represented by a square with a radius of 30 units.
# 1 V 1 Environment
![1 V 1 Environment](https://github.com/Aman8T/AI-Soccer/blob/main/football%20environmnet.png)  
# Game Rules
The game is played in a total of 180 seconds (can be changed).
After the winner announcement, the scores are displayed and the game is reset to 0-0 after a span of 10 seconds and the robots take random positions in their respective halves. 
(Random position was introduced to improve the generalization of the model)

# Game Setup
![Game Setup](https://github.com/Aman8T/AI-Soccer/assets/77984568/473f27da-e3e3-4ff1-9802-3210f569d1e2)

# Reinforcement Leaning Setup
![Project Logiv](https://github.com/Aman8T/AI-Soccer/assets/77984568/fd3603f8-0ecf-4982-95d0-50f4e3dec702)

# States(12)
Array [
Robot direction-> up, down, right, left
Ball w.r.t Ai agent->up, down, right, left
Goal Post w.r.t Ai agent->up, down, right, left
]

# Actions(4)
Move-> Straight, Right, Left, Backwards

# Reward Function:
+100 for scoring a goal
-50 for conceding
-distance of the robot from the ball ( to motivate the robot to stay closer to the ball)

# Procedure and Theory:
Reinforcement learning (RL) is an area of machine learning concerned with how software agents ought to take actions in an environment in order to maximize the notion of cumulative reward.
Thus, RL  teaches a software agent how to behave in an environment by telling it how good it’s doing.
Deep Q-learning is a type of reinforcement learning algorithm that uses a deep neural network to approximate the Q-function, which is used to determine the optimal action to take in a given state. The Q-function represents the expected cumulative reward of taking a certain action in a certain state and following a certain policy. In Q-Learning, the Q-function is updated iteratively as the agent interacts with the environment. Deep Q-Learning is used in various applications such as game playing, robotics, and autonomous vehicles.
Deep Q-learning is a variant of Q-learning that uses a deep neural network to represent the Q-function, rather than a simple table of values. This allows the algorithm to handle environments with a large number of states and actions, as well as to learn from high-dimensional inputs such as images or sensor data.
Model: Linear neural network with fully connected input, hidden, and output layers.
Model: 12->256 ->128->4

# Results:
![Results](https://github.com/Aman8T/AI-Soccer/assets/77984568/f071f9dd-4103-481f-a1c4-54b667c70ebd)






