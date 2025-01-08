import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores, highest_tiles):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label="Score")
    plt.plot(mean_scores, label="Average score")
    plt.plot(highest_tiles, label="Highest tile")
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.text(len(highest_tiles)-1, highest_tiles[-1], str(highest_tiles[-1]))
    plt.legend(loc="upper left")
    plt.pause(0.1)
