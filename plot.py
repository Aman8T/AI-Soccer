import matplotlib.pyplot as plt
from IPython import display
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

plt.ion()

def plot(score1,score2, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(score1)
    plt.plot(score2)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(score1)-1, score1[-1], str(score1[-1]))
    plt.text(len(score2)-1, score2[-1], str(score2[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)