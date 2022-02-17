from Environment_Class import Traffic_Signal_Control
import matplotlib.pyplot as plt

print_interval = 10
plt_episodeAve = []
plt_aveScore = []

def main():
    env = Traffic_Signal_Control()
    #score = 0.0
    for n_epi in range(100):
        print(n_epi)
        for action in range(0, 8):
            state_prime, reward, done = env.step(action)
            state = state_prime
            score = reward
        if n_epi % print_interval == 0 and n_epi != 0:
            plt_episodeAve.append(n_epi)
            plt_aveScore.append(score)
            #score = 0.0
            print(plt_aveScore)
            print(plt_episodeAve)

if __name__ == '__main__':
    main()
    plt.plot(plt_episodeAve, plt_aveScore)
    plt.xlabel('episode')
    plt.ylabel('average_reward')
    plt.show()
