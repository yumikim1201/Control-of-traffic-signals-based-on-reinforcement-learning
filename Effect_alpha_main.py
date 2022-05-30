from Effect_alpha_env import Traffic_Signal_Control
import collections
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

plt_TimeRLTSC = []
plt_NumRLTSC = []
plt_TimeRL = []
plt_NumRL = []

alpha = [0.0, 0.5, 1.0]

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
        self.fc1 = nn.Linear(16, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 8)

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
    for i in range(0, 3):
        # CartPole 환경 구성
        env = Traffic_Signal_Control()

        # 모델 불러오기
        q = Qnet()
        q_target = Qnet()
        q_target.load_state_dict(q.state_dict())
        memory = ReplayBuffer()

        optimizer = optim.Adam(q.parameters(), lr=learning_rate)
        check = 0
        for n_epi in range(4000):
            print(n_epi)
            epsilon = max(0.01, 0.08 - 0.01 * (n_epi / 200))  # Linear annealing from 8% to 1%
            state = env.reset()
            done = False
            t = 1
            while not done:
                action = q.sample_action(torch.tensor(state).float(), epsilon)
                state_prime, reward, next_Time, next_Num, done = env.step(action, alpha[i], check)  # 선택된 action -> return
                done_mask = 0.0 if done else 1.0
                memory.put((state, action, reward, state_prime, done_mask))  # memory append
                state = state_prime
                if done or t == 500:
                    break
                t = t + 1
            if memory.size() > 2000:  # episode 4회 이상
                train(q, q_target, memory, optimizer, n_epi)

            if n_epi % print_interval == 0 and n_epi != 0:
                q_target.load_state_dict(q.state_dict())
        plt_TimeRLTSC.append(next_Time)
        plt_NumRLTSC.append(next_Num)
        print(plt_TimeRLTSC)
        print(plt_NumRLTSC)
####################################################################################
        # CartPole 환경 구성
        env = Traffic_Signal_Control()
        # 모델 불러오기
        q = Qnet()
        q_target = Qnet()
        q_target.load_state_dict(q.state_dict())
        memory = ReplayBuffer()

        optimizer = optim.Adam(q.parameters(), lr=learning_rate)
        check = 1
        for n_epi in range(4000):
            print(n_epi)
            epsilon = max(0.01, 0.08 - 0.01 * (n_epi / 200))  # Linear annealing from 8% to 1%
            state = env.reset()
            done = False
            t = 1
            while not done:
                action = q.sample_action(torch.tensor(state).float(), epsilon)
                state_prime, reward, next_Time, next_Num, done = env.step(action, alpha[i], check)  # 선택된 action -> return
                done_mask = 0.0 if done else 1.0
                memory.put((state, action, reward, state_prime, done_mask))  # memory append
                state = state_prime
                if done or t == 500:
                    break
                t = t + 1
            if memory.size() > 2000:  # episode 4회 이상
                train(q, q_target, memory, optimizer, n_epi)

            if n_epi % print_interval == 0 and n_epi != 0:
                q_target.load_state_dict(q.state_dict())
        plt_TimeRL.append(next_Time)
        plt_NumRL.append(next_Num)
        print(plt_TimeRL)
        print(plt_NumRL)



if __name__ == '__main__':
    main()
    plt.figure(1)
    plt.plot(alpha, plt_NumRLTSC, 'r*-', label='RL-TSC')
    plt.plot(alpha, plt_NumRL, 'b^-', label='FIX')
    plt.xlabel('Alpha')
    plt.ylabel('Num')
    #plt.ylim([0, 200])
    plt.legend(loc='best', ncol=1)
    plt.savefig('./Alpha(Num).png')

    plt.figure(2)
    plt.plot(alpha, plt_TimeRLTSC, 'r*-', label='RL-TSC')
    plt.plot(alpha, plt_TimeRL, 'b^-', label='FIX')
    plt.xlabel('Alpha')
    plt.ylabel('Time')
    # plt.ylim([0, 3000])
    plt.legend(loc='best', ncol=1)
    plt.savefig('./Alpha(Time).png')