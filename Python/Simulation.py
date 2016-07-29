#Simulation of Index Coding system with N nodes
#Author: Barak Lidsky
import numpy as np
import SVD
import SVD_enc

class Node:

    def __init__(self, number, tot, P, p):
        self.num = number
        self.total = tot
        self.messages = np.zeros((1, self.total))
        self.X = np.zeros((self.total, 1))
        self.M = 0
        self.mess = 0
        self.p = P
        self.p2 = p

    def get_mess_APIC(self, message, number):
        p = np.random.random()
        if (p < self.p2) and number != self.num:
            self.messages[0][number] = message
            return 1
        else:
            return 0

    def get_mess_RR(self, message, number):
        p = np.random.random()
        if (p < self.p2):
            self.messages[0][number] = message
            return 1
        else:
            return 0

    def get_mess_RR2(self, message, number):
        p = np.random.random()
        if (p < self.p):
            self.messages[0][number] = message
            return 1
        else:
            return 0

    def get_x(self, x, number):
        p = np.random.random()
        if (p < self.p) :
            self.X[number][0] = x
            return 1
        else:
            return 0

    def get_M(self, M):
        p = np.random.random()
        if (p < self.p):
            self.M = M.copy()
            return 1
        else:
            return 0

    def recover_mess(self):
        self.mess = SVD_enc.SVDdec(self.M, self.X, self.num, self.messages)


def simulation_APIC(N, p):
    #Simulation of APIC message sending with SVD decoding
    #Initialize Nodes
    Nodes = []
    for i in range(N):
        Nodes.append(Node(i, N, p, .8))
    #random messages
    T = np.random.rand(N, 1)
    #first round of sending messages
    M = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            temp = Nodes[j].get_mess_APIC(T[i][0], i)
            if temp == 1 and i != j:
                M[j][i] = 2
            if temp == 1 and i == j:
                M[j][i] = 1
    #APIC
    [Rmin, OptM] = SVD.APIndexCode(M)
    #SVD encoding
    X = SVD_enc.SVDenc(OptM, T, Rmin)
    #construct A, matrix of sideinfo with actual messages
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if M[i][j] == 2:
                A[i][j] = T[j][0]
    #send X and M until all receivers have them
    end = 1
    #X by N empty matrix, will fill with 1s until everyone has all of X
    U = np.zeros((len(X),N))
    #empty array, will fill with 1s until everyone has M
    G = np.zeros((1, N))
    #Init
    count = 0
    round = 0
    while(end):
        #Send all messages of X
        for i in range(len(X)):
            tem = U[i][:]
            left = np.nonzero(tem == 0)
            #If everyone has X message, don't resend it
            if len(left[0]) > 0:
                count += 1
                for j in range(N):
                    if Nodes[j].X[i][0] == 0:
                        temp = Nodes[j].get_x(X[i][0], i)
                        if temp == 1:
                            U[i][j] = 1
        #Send M to everyone
        numleft = np.nonzero(G == 0)
        #If everyone has M, don't resend it
        if len(numleft[0]) > 0:
            count += 1
            for i in range(N):
                if G[0][i] == 0:
                    temp = Nodes[i].get_M(OptM)
                    if temp == 1:
                        G[0][i] = 1
        #increment round
        round +=1
        zeros = np.nonzero(U == 0)
        #If everyone has all the messages, exit while loop of sending
        if len(zeros[0]) == 0 and len(numleft[0]) == 0:
            end = 0

    for i in range(N):
        #nodes recover their messages
        Nodes[i].recover_mess()

    #check results
    '''
    for i in range(N):
        #print(i)
        print("rec: ", Nodes[i].mess, "t: ", T[i][0], "diff: ", abs(Nodes[i].mess - T[i][0]))
    print("Rounds: ", round, "count: ", count, "N: ", N, "Rmin: ", Rmin)
    '''
    return (round, count, Rmin)

#[Round, Count, Rmin] = simulation(14)

def simulation_RR(N, p):
    #Simulation of Round Robin message sending
    Nodes = []
    for i in range(N):
        Nodes.append(Node(i, N, p, .8))
    # random messages
    T = np.random.rand(N, 1)
    M = np.zeros((N, N))
    count = -N
    round = -1
    exit = 1
    while(exit):
        for i in range(N):
            # IF the receiver that wants the message, has it, don't resend
            if M[i][i] == 0:
                count += 1
                for j in range(N):
                    if Nodes[j].X[i][0] == 0:
                        if round == -1:
                            temp = Nodes[j].get_mess_RR(T[i][0], i)
                        else:
                            temp = Nodes[j].get_mess_RR2(T[i][0], i)
                        if temp == 1 and i == j:
                            M[i][j] = 1
                        if temp == 1 and i != j:
                            M[i][j] = 2
        round += 1
        diag = np.nonzero(M == 1)
        if len(diag[0]) == N:
            exit = 0
    return (round, count)





def test_sim(N):
    P = [.1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7]
    ite = 50
    avgRound_APIC = []
    avgRound_RR = []
    avgCount_APIC = []
    avgCount_RR = []
    avgRmin = []
    for prob in P:
        sumRound_APIC = 0
        sumCount_APIC = 0
        sumRound_RR = 0
        sumCount_RR = 0
        sumRmin = 0
        for i in range(ite):
            print(i)
            [Round_APIC, Count_APIC, Rmin] = simulation_APIC(N, prob)
            [Round_RR, Count_RR] = simulation_RR(N, prob)
            sumRound_APIC += Round_APIC
            sumRound_RR += Round_RR
            sumCount_APIC += Count_APIC
            sumCount_RR += Count_RR
            sumRmin +=Rmin
        avgRound_APIC.append(sumRound_APIC/ite)
        avgRound_RR.append(sumRound_RR/ite)
        avgCount_APIC.append(sumCount_APIC/ite)
        avgCount_RR.append(sumCount_RR/ite)
        avgRmin.append(sumRmin/ite)
    for j in range(len(P)):
        print("round: ", avgRound_APIC[j], "count: ", avgCount_APIC[j], "rmin: ", avgRmin[j])
        print("round: ", avgRound_RR[j], "count: ", avgCount_RR[j])
        print("Round ThroPut: ", (avgRound_RR[j]- avgRound_APIC[j])/avgRound_RR[j]*100, "Count ThoPut: ", (avgCount_RR[j]- avgCount_APIC[j])/avgCount_RR[j]*100)

#test_sim(14)

def sim_test_once(N):
    ite = 50
    avgRound_APIC = []
    avgRound_RR = []
    avgCount_APIC = []
    avgCount_RR = []
    avgRmin = []

    sumRound_APIC = 0
    sumCount_APIC = 0
    sumRound_RR = 0
    sumCount_RR = 0
    sumRmin = 0
    prob = .9
    for i in range(ite):
        print(i)
        [Round_APIC, Count_APIC, Rmin] = simulation_APIC(N, prob)
        [Round_RR, Count_RR] = simulation_RR(N, prob)
        sumRound_APIC += Round_APIC
        sumRound_RR += Round_RR
        sumCount_APIC += Count_APIC
        sumCount_RR += Count_RR
        sumRmin += Rmin
    avgRound_APIC.append(sumRound_APIC / ite)
    avgRound_RR.append(sumRound_RR / ite)
    avgCount_APIC.append(sumCount_APIC / ite)
    avgCount_RR.append(sumCount_RR / ite)
    avgRmin.append(sumRmin / ite)

    print("round: ", avgRound_APIC[0], "count: ", avgCount_APIC[0], "rmin: ", avgRmin[0])
    print("round: ", avgRound_RR[0], "count: ", avgCount_RR[0])
    print("Round ThroPut: ", (avgRound_RR[0] - avgRound_APIC[0]) / avgRound_RR[0] * 100, "Count ThoPut: ",(avgCount_RR[0] - avgCount_APIC[0]) / avgCount_RR[0] * 100)

sim_test_once(10)
