import random

# Hyperparameters

time_theta = 0.3

K = 30 #한번 신호가 열렸을 때 차량의 처리율

seconds = 30  #신호 주기 == K배 (00초에 1대)

class Traffic_Signal_Control():
    def __init__(self):

        self.LeftNum = []
        self.LeftNum.append(random.randint(1, 50))
        self.LeftNum.append(random.randint(1, 50))
        self.LeftNum.append(random.randint(1, 50))
        self.LeftNum.append(random.randint(1, 50))

        self.StraightNum = []
        self.StraightNum.append(random.randint(1, 50))
        self.StraightNum.append(random.randint(1, 50))
        self.StraightNum.append(random.randint(1, 50))
        self.StraightNum.append(random.randint(1, 50))


        self.LeftTime = []
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[0]):
            self.LeftTime[0].append(random.randint(1, 50))
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[1]):
            self.LeftTime[1].append(random.randint(1, 50))
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[2]):
            self.LeftTime[2].append(random.randint(1, 50))
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[3]):
            self.LeftTime[3].append(random.randint(1, 50))

        for i in range(0, 4):
            self.LeftTime[i].sort()

        self.StraightTime = []
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[0]):
            self.StraightTime[0].append(random.randint(1, 50))
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[1]):
            self.StraightTime[1].append(random.randint(1, 50))
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[2]):
            self.StraightTime[2].append(random.randint(1, 50))
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[3]):
            self.StraightTime[3].append(random.randint(1, 50))

        for i in range(0, 4):
            self.StraightTime[i].sort()

    def sum_of_state_by_aciton(self):
        list_Numsum = []
        list_Timesum = []
        #print("SN", self.StraightNum)
        #print("LN", self.LeftNum)

        list_Numsum.append(self.StraightNum[1] + self.StraightNum[3])
        list_Numsum.append(self.StraightNum[0] + self.StraightNum[2])
        list_Numsum.append(self.LeftNum[0] + self.StraightNum[0])
        list_Numsum.append(self.LeftNum[1] + self.StraightNum[1])
        list_Numsum.append(self.LeftNum[2] + self.StraightNum[2])
        list_Numsum.append(self.LeftNum[3] + self.StraightNum[3])
        list_Numsum.append(self.LeftNum[1] + self.LeftNum[3])
        list_Numsum.append(self.LeftNum[0] + self.LeftNum[2])

        #print("ST", self.StraightTime)
        #print("LT", self.LeftTime)
        list_Timesum.append(self.StraightTime[1][0] + self.StraightTime[3][0])
        list_Timesum.append(self.StraightTime[0][0] + self.StraightTime[2][0])
        list_Timesum.append(self.LeftTime[0][0] + self.StraightTime[0][0])
        list_Timesum.append(self.LeftTime[1][0] + self.StraightTime[1][0])
        list_Timesum.append(self.LeftTime[2][0] + self.StraightTime[2][0])
        list_Timesum.append(self.LeftTime[3][0] + self.StraightTime[3][0])
        list_Timesum.append(self.LeftTime[1][0] + self.LeftTime[3][0])
        list_Timesum.append(self.LeftTime[0][0] + self.LeftTime[2][0])

        return(list_Numsum, list_Timesum)

    def step(self, action):
        list_num, list_time = self.sum_of_state_by_aciton()

        """
        for i in range(0, 4):
            if 0 in self.StraightTime[i]:
                self.StraightTime[i] = []
            if 0 in self.LeftTime[i]:
                self.LeftTime[i] = []
        if max(list_time) >= time_theta:
            for i in range(0, 8):
                if max(list_time) == list_time[i]:
                    action = i
        """
        if action == 0:
            self.move_StraightOdd()

        elif action == 1:
            self.move_StraightEven()

        elif action == 2:
            self.move_StraightLeft0()

        elif action == 3:
            self.move_StraightLeft1()

        elif action == 4:
            self.move_StraightLeft2()

        elif action == 5:
            self.move_StraightLeft3()

        elif action == 6:
            self.move_LeftOdd()

        elif action == 7:
            self.move_LeftEven()

        for i in range(0, 4):
            if not self.StraightTime[i]:
                self.StraightTime[i] = [0]
            if not self.LeftTime[i]:
                self.LeftTime[i] = [0]

        leftTime = 0
        straightTime = 0
        for i in range(0, 4):
            leftTime += self.LeftTime[i][0]
            straightTime += self.StraightTime[i][0]

        next_Time = leftTime + straightTime
        next_Num = self.StraightNum + self.LeftNum

        #reward = - sum(next_Num) 16
        #reward = - next_Time #300
        reward = -(0.8 * sum(next_Num) + 0.2 * next_Time)

        #print(reward)
        if reward >= -300:
            done = True
        else:
            done = False

        #print(self.StraightTime)
        #print(self.LeftTime)

        return (self.LeftNum[0], self.LeftNum[1], self.LeftNum[2], self.LeftNum[3]
            , self.StraightNum[0], self.StraightNum[1], self.StraightNum[2], self.StraightNum[3]
            , self.LeftTime[0][0], self.LeftTime[1][0], self.LeftTime[2][0], self.LeftTime[3][0]
            , self.StraightTime[0][0], self.StraightTime[1][0], self.StraightTime[2][0], self.StraightTime[3][0]
        ), reward, done

    def move_StraightOdd(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.StraightNum[1] = self.StraightNum[1] - K
        self.StraightNum[3] = self.StraightNum[3] - K

        if self.StraightNum[1] < 0:
            self.StraightNum[1] = 0

        if self.StraightNum[3] < 0:
            self.StraightNum[3] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[0]
            self.LeftNum[i] = self.LeftNum[i] + gamma[0]

        if len(self.StraightTime[1]) >= K and len(self.StraightTime[3]) >= K:
            del self.StraightTime[1][:K]
            del self.StraightTime[3][:K]

        else:
            if len(self.StraightTime[1]) <= K:
                self.StraightTime[1] = [0]

            if len(self.StraightTime[3]) <= K:
                self.StraightTime[3] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[0]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[0]):
                self.LeftTime[j].append(1)

    def move_StraightEven(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.StraightNum[0] = self.StraightNum[0] - K
        self.StraightNum[2] = self.StraightNum[2] - K

        if self.StraightNum[0] < 0:
            self.StraightNum[0] = 0

        if self.StraightNum[2] < 0:
            self.StraightNum[2] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[1]
            self.LeftNum[i] = self.LeftNum[i] + gamma[1]

        if len(self.StraightTime[0]) >= K and len(self.StraightTime[2]) >= K:
            del self.StraightTime[0][:K]
            del self.StraightTime[2][:K]

        else:
            if len(self.StraightTime[0]) <= K:
                self.StraightTime[0] = [0]
            if len(self.StraightTime[2]) <= K:
                self.StraightTime[2] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[1]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[1]):
                self.LeftTime[j].append(1)

    def move_StraightLeft0(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.StraightNum[0] = self.StraightNum[0] - K
        self.LeftNum[0] = self.LeftNum[0] - K

        if self.StraightNum[0] < 0:
            self.StraightNum[0] = 0

        if self.LeftNum[0] < 0:
            self.LeftNum[0] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[2]
            self.LeftNum[i] = self.LeftNum[i] + gamma[2]

        if len(self.StraightTime[0]) >= K and len(self.LeftTime[0]) >= K:
            del self.StraightTime[0][:K]
            del self.LeftTime[0][:K]

        else:
            if len(self.StraightTime[0]) <= K:
                self.StraightTime[0] = [0]
            if len(self.LeftTime[0]) <= K:
                self.LeftTime[0] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[2]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[2]):
                self.LeftTime[j].append(1)

    def move_StraightLeft1(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.StraightNum[1] = self.StraightNum[1] - K
        self.LeftNum[1] = self.LeftNum[1] - K

        if self.StraightNum[1] < 0:
            self.StraightNum[1] = 0

        if self.LeftNum[1] < 0:
            self.LeftNum[1] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[3]
            self.LeftNum[i] = self.LeftNum[i] + gamma[3]

        if len(self.StraightTime[1]) >= K and len(self.LeftTime[1]) >= K:
            del self.StraightTime[1][:K]
            del self.LeftTime[1][:K]
        else:
            if len(self.StraightTime[1]) <= K:
                self.StraightTime[1] = [0]
            if len(self.LeftTime[1]) <= K:
                self.LeftTime[1] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[3]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[3]):
                self.LeftTime[j].append(1)

    def move_StraightLeft2(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.StraightNum[2] = self.StraightNum[2] - K
        self.LeftNum[2] = self.LeftNum[2] - K

        if self.StraightNum[2] < 0:
            self.StraightNum[2] = 0

        if self.LeftNum[2] < 0:
            self.LeftNum[2] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[4]
            self.LeftNum[i] = self.LeftNum[i] + gamma[4]

        if len(self.StraightTime[2]) >= K and len(self.LeftTime[2]) >= K:
            del self.StraightTime[2][:K]
            del self.LeftTime[2][:K]
        else:
            if len(self.StraightTime[2]) <= K:
                self.StraightTime[2] = [0]
            if len(self.LeftTime[2]) <= K:
                self.LeftTime[2] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[4]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[4]):
                self.LeftTime[j].append(1)

    def move_StraightLeft3(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.StraightNum[3] = self.StraightNum[3] - K
        self.LeftNum[3] = self.LeftNum[3] - K

        if self.StraightNum[3] < 0:
            self.StraightNum[3] = 0

        if self.LeftNum[3] < 0:
            self.LeftNum[3] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[5]
            self.LeftNum[i] = self.LeftNum[i] + gamma[5]

        if len(self.StraightTime[3]) >= K and len(self.LeftTime[3]) >= K:
            del self.StraightTime[3][:K]
            del self.LeftTime[3][:K]
        else:
            if len(self.StraightTime[3]) <= K:
                self.StraightTime[3] = [0]
            if len(self.LeftTime[3]) <= K:
                self.LeftTime[3] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[5]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[5]):
                self.LeftTime[j].append(1)

    def move_LeftOdd(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.LeftNum[1] = self.LeftNum[1] - K
        self.LeftNum[3] = self.LeftNum[3] - K

        if self.LeftNum[1] < 0:
            self.LeftNum[1] = 0

        if self.LeftNum[3] < 0:
            self.LeftNum[3] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[6]
            self.LeftNum[i] = self.LeftNum[i] + gamma[6]

        if len(self.LeftTime[1]) >= K and len(self.LeftTime[3]) >= K:
            del self.LeftTime[1][:K]
            del self.LeftTime[3][:K]
        else:
            if len(self.LeftTime[1]) <= K:
                self.LeftTime[1] = [0]
            if len(self.LeftTime[3]) <= K:
                self.LeftTime[3] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[6]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[6]):
                self.LeftTime[j].append(1)

    def move_LeftEven(self):
        gamma = []
        for i in range(0, 8):
            gamma.append(random.randint(1, 10))
        self.LeftNum[0] = self.LeftNum[0] - K
        self.LeftNum[2] = self.LeftNum[2] - K

        if self.LeftNum[0] < 0:
            self.LeftNum[0] = 0

        if self.LeftNum[2] < 0:
            self.LeftNum[2] = 0

        for i in range(0, 4):
            self.StraightNum[i] = self.StraightNum[i] + gamma[7]
            self.LeftNum[i] = self.LeftNum[i] + gamma[7]

        if len(self.LeftTime[0]) >= K and len(self.LeftTime[2]) >= K:
            del self.LeftTime[0][:K]
            del self.LeftTime[2][:K]
        else:
            if len(self.LeftTime[0]) <= K:
                self.LeftTime[0] = [0]
            if len(self.LeftTime[2]) <= K:
                self.LeftTime[2] = [0]

        for j in range(0, 4):
            for i in range(0, len(self.StraightTime[j])):
                if self.StraightTime[j][i] != 0:
                    self.StraightTime[j][i] = self.StraightTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, len(self.LeftTime[j])):
                if self.LeftTime[j][i] != 0:
                    self.LeftTime[j][i] = self.LeftTime[j][i] + seconds

        for j in range(0, 4):
            for i in range(0, gamma[7]):
                self.StraightTime[j].append(1)

        for j in range(0, 4):
            for i in range(0, gamma[7]):
                self.LeftTime[j].append(1)

    def reset(self):

        self.LeftNum = []
        self.LeftNum.append(random.randint(1, 20))
        self.LeftNum.append(random.randint(1, 20))
        self.LeftNum.append(random.randint(1, 20))
        self.LeftNum.append(random.randint(1, 20))

        self.StraightNum = []
        self.StraightNum.append(random.randint(1, 20))
        self.StraightNum.append(random.randint(1, 20))
        self.StraightNum.append(random.randint(1, 20))
        self.StraightNum.append(random.randint(1, 20))

        self.LeftTime = []
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[0]):
            self.LeftTime[0].append(random.randint(1, 20))
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[1]):
            self.LeftTime[1].append(random.randint(1, 20))
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[2]):
            self.LeftTime[2].append(random.randint(1, 20))
        self.LeftTime.append([])
        for i in range(0, self.LeftNum[3]):
            self.LeftTime[3].append(random.randint(1, 20))

        for i in range(0, 4):
            self.LeftTime[i].sort()

        self.StraightTime = []
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[0]):
            self.StraightTime[0].append(random.randint(1, 20))
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[1]):
            self.StraightTime[1].append(random.randint(1, 20))
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[2]):
            self.StraightTime[2].append(random.randint(1, 20))
        self.StraightTime.append([])
        for i in range(0, self.StraightNum[3]):
            self.StraightTime[3].append(random.randint(1, 20))

        for i in range(0, 4):
            self.StraightTime[i].sort()

        return (self.LeftNum[0], self.LeftNum[1], self.LeftNum[2], self.LeftNum[3]
                , self.StraightNum[0], self.StraightNum[1], self.StraightNum[2], self.StraightNum[3]
                , self.LeftTime[0][0], self.LeftTime[1][0], self.LeftTime[2][0], self.LeftTime[3][0]
                , self.StraightTime[0][0], self.StraightTime[1][0], self.StraightTime[2][0], self.StraightTime[3][0]
               )
