from Effect_gammaInput_env import Traffic_Signal_Control
import collections
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

plt_aveRLTSC = []
plt_aveFTTSC = []

gamma_input = [2, 4, 6, 8, 10]

# Hyperparameters
learning_rate = 0.0005
gamma = 0.98
buffer_limit = 50000
batch_size = 32
print_interval = 50

class ReplayBuffer():
    def __init__(self):
        self.buffer = collections.deque(maxlen=buffer_limit)

    def put(self, transition):
        self.buffer.append(transition)

    def sample(self, n):
        mini_batch = random.sample(self.buffer, n)
        s_lst, a_lst, r_lst, s_prime_lst, done_mask_lst = [], [], [], [], []

        for transition in mini_batch:
            s, a, r, s_prime, done_mask = transition
            s_lst.append(s)
            a_lst.append([a])
            r_lst.append([r])
            s_prime_lst.append(s_prime)
            done_mask_lst.append([done_mask])

        return torch.tensor(s_lst, dtype=torch.float), torch.tensor(a_lst), \
               torch.tensor(r_lst), torch.tensor(s_prime_lst, dtype=torch.float), \
               torch.tensor(done_mask_lst)

    def size(self):
        return len(self.buffer)


class Qnet(nn.Module):
    def __init__(self):
        super(Qnet, self).__init__()
        self.fc1 = nn.Linear(16, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 16)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        coin = random.random()
        if coin < epsilon:
            return random.randint(0, 7)  # 0 ~ 7
        else:
            return out.argmax().item()  # 뉴럴 네트워크의 max값


def train(q, q_target, memory, optimizer, n_epi):  # Q-learning으로 학습 -> target설정
    for i in range(10):
        state, action, reward, state_prime, done_mask = memory.sample(batch_size)

        q_out = q(state)
        q_action = q_out.gather(1, action)
        max_q_prime = q_target(state_prime).max(1)[0].unsqueeze(1)
        target = reward + gamma * max_q_prime * done_mask
        loss = F.smooth_l1_loss(q_action, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()



def main():
    # CartPole 환경 구성
    env = Traffic_Signal_Control()

    # 모델 불러오기
    q = Qnet()
    q_target = Qnet()
    q_target.load_state_dict(q.state_dict())
    memory = ReplayBuffer()

    optimizer = optim.Adam(q.parameters(), lr=learning_rate)
    for i in range(0, 5):
        score = 0.0
        for n_epi in range(6000):
            print(n_epi)
            epsilon = max(0.01, 0.08 - 0.01 * (n_epi / 200))  # Linear annealing from 8% to 1%
            state = env.reset()
            done = False
            t = 1
            while not done:
                action = q.sample_action(torch.tensor(state).float(), epsilon)
                #print(action)
                state_prime, reward, done = env.step(action, gamma_input[i])  # 선택된 action -> return
                #print(reward)
                done_mask = 0.0 if done else 1.0
                memory.put((state, action, reward, state_prime, done_mask))  # memory append
                state = state_prime
                score += reward
                if done or t == 3000:
                    break
                t = t + 1
            if memory.size() > 3000:  # episode 4회 이상
                train(q, q_target, memory, optimizer, n_epi)

            if n_epi % print_interval == 0 and n_epi != 0:
                q_target.load_state_dict(q.state_dict())
        plt_aveRLTSC.append(reward)
        print(plt_aveRLTSC)
    #env.close()

        score = 0.0
        for n_epi in range(100):
            print(n_epi)
            for action in range(0, 8):
                state_prime, reward, done = env.step(action, gamma_input[i])
                state = state_prime
                score = reward
        plt_aveFTTSC.append(-score/10)
        # score = 0.0
        print(plt_aveFTTSC)

if __name__ == '__main__':
    main()
    plt.plot(gamma_input, plt_aveRLTSC, 'r*-', label='RLTSC')
    plt.plot(gamma_input, plt_aveFTTSC, 'b^-', label='FTTSC/100')
    plt.xlabel('gamma')
    plt.ylabel('average_reward')
    plt.ylim([10, 30000])
    plt.legend(loc='best', ncol=1)
    plt.show()