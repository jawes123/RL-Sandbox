import random


# TD Learning:
#   initialize value fn to 0
#   use time-varying scalar step-size of αt = 1/N(st, at)
#   ε-greedy exploration strategy with εt = N0/(N0 + N(st)), 
#       where N0 = 100 is constant (can adjust)
#       N(s) is number of times state s has been visited
#       N(s, a) is number of times that action a has been selected from state s
#   
#   Plan:
#       Prediction:
#           For each episode:
#               E(s,a) = 0
#               Initialize S, A
#               For each step of episode:
#                   Take action A, observe R, S'
#                   Choose A' from S' using policy derived from Q (e.g. e-greedy)
#                   TD-error = R + Q(S',A') - Q(S,A)
#                   E(S,A) = E(S,A) + 1
#                   For each visited s and a:
#                       ???? confused. watch video (lecture 5)
#       Control: Use ε-greedy(Q) to find best Q fn out of set of Q's
#           with prob ε choose action at rand, with prob 1-ε choose greedy


############## Constants ##############
N0 = 100
HIT = "HIT"
STAND = "STAND"
LAMBDA = [n/10 for n in range(11)]
#######################################


################ Logic ################
# game start
def main():
    # iterate thru each value of λ
    # num_s = dict storing # of times each state s has been visited; {(int,int):int}
    num_s = {}
    # num_sa = dict storing # of times action a has been taken at state s;
    #   {((int,int),str):int}
    num_sa = {}
    # e_trace = dict storing previously calculated eligibility trace for each state-action
    #   {((int, int),str):int}
    e_trace = {}
    # action_val = dict storing previous Q(s,a) calculated when taking a particular a at particular s
    #   {((int,int),str):int}
    action_val = {}

    for l in LAMBDA:
        for i in range(1000):
            # list storing complete history of state-actions and rewards for each episode
            visited = []
            # initial state = tuple(dealer, player)
            next_s = (draw(), draw())
            # get action based on existing action-value fn
            next_a = next_action(next_s)
            while((x := step(next_s, next_a))[1] == float('-inf')):
                # update num_s, num_sa, e_trace, visited, action_val
                visited.append(x)
                state = x[0]

                # increment and update num_s for this state (meaning visited this state 1 more time)
                num_s.setdefault(state, 0)
                num_s[state] = num_s[state]+1
                # initialize action_val to 0 for both hit and stand for this state if not existing
                action_val.setdefault((state, HIT), 0)
                action_val.setdefault((state, STAND), 0)
                # e-greedy exploration with et = N0/(N0 + N(st))
                epsilon = N0 / (N0 + num_s[state])


        # call step
        # every single time step return to update
    return


def next_action(state):
    return


def draw():
    return random.randint(1, 10)


# Parameters: 
#   state (dealer's first card 1-10 and the player's sum 1-21)
#   action (hit or stand)
# Returns: ((dealer, player),reward)
#   sample of the next state s' (may be terminal if game finished)
#   AND reward r
def step(state, action):

    # state is a tuple
    dealer = state[0]
    player = state[1]
    reward = float('-inf')

    # if previous action was stand
    if action == "STAND":
        while(dealer < 17 and dealer >= 1):
            # calculating dealer's next card. must first pick random card 1-10
            dealer_next = draw()
            # then determine if it is red (1/3) or black (2/3)
            dealer_next = dealer_next*-1 if random.randint(1,3) == 1 else dealer_next
            dealer += dealer_next

        # if dealer busts
        if dealer < 1 or dealer > 21:
            reward = 1
        
        # if dealer doesn't bust, higher sum wins
        if dealer < player: reward = 1
        elif dealer > player: reward = -1
        else: reward = 0
    
    # if previous action was hit
    elif action == "HIT":
        player_next = draw()
        player_next = player_next*-1 if random.randint(1,3) == 1 else player_next
        player += player_next

        # if player busts
        if player < 1 or player > 21:
            reward = -1

    # return next state and reward
    next_s = (dealer, player)
    return (next_s, reward)

#######################################

if __name__ == '__main__':
    main()