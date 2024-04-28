
import random
import game
import matplotlib.pyplot as plt
import numpy as np

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
N0 = 10
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
        print(f"******* LAMBDA = {l} *******")
        cum_reward = 0
        for i in range(1000):
            # list storing complete history of state-actions and rewards for each episode
            visited = []
            # initial state = tuple(dealer, player)
            state = (game.draw(), game.draw())
            # get action based on existing action-value fn
            next_a = next_action(state, num_s, num_sa, e_trace, action_val, visited)
            step_return = None
            while((step_return := game.step(state, next_a))[1] == float('-inf')):
                # update num_s, num_sa, e_trace, visited, action_val
                state = step_return[0]
                next_a = next_action(state, num_s, num_sa, e_trace, action_val, visited)
            
            # calculate and update action-value
            reward = step_return[1]
            update_q(visited, reward, num_sa, e_trace, action_val, l)

            # track cumulative reward across eps; every 100 eps print out
            cum_reward += reward
            if i % 100 == 0:
                print(f'The cumulative reward at episode {i}: {cum_reward}')
    return

# Updates all relevant data structures for current state-action and returns next action
def next_action(state, num_s, num_sa, e_trace, action_val, visited):
    # increment and update num_s for this state (meaning visited this state 1 more time)
    num_s.setdefault(state, 0)
    num_s[state] = num_s[state]+1
    # 
    # initialize action_val to 0 for both hit and stand for this state if not existing
    action_val.setdefault((state, HIT), 0)
    action_val.setdefault((state, STAND), 0)

    # calculate new et = N0/(N0 + N(st)) to pass to next_action
    epsilon = N0 / (N0 + num_s[state])

    # Control: Use e-greedy(Q) to find best Q fn out of set of Q's;
    #   With prob epsilon choose action at rand, with prob 1-e choose greedy
    if random.random() <= epsilon or action_val[(state, HIT)] == action_val[(state, STAND)]:
        next_a = random.choice([HIT, STAND])
    else:
        next_a = HIT if action_val[(state, HIT)] > action_val[(state, STAND)] else STAND
    
    # update num_sa, e_trace, and visited (same concept as updating num_s) with newly obtained action
    num_sa.setdefault((state, next_a), 0)
    num_sa[(state, next_a)] = num_sa[(state, next_a)] + 1
    e_trace.setdefault((state, next_a), 0)
    e_trace[(state, next_a)] = e_trace[(state, next_a)] + 1
    visited.append((state, next_a))
    return next_a

# recursively update Q values of all previously visited state-actions in the episode
def update_q(visited, reward, num_sa, e_trace, action_val, l):
    if not visited:
        # since terminal state, there is no Q value, so return the reward instead
        return reward
    
    state_action = visited[0]
    q_sa_prime = update_q(visited[1:], reward, num_sa, e_trace, action_val, l)

    # calculate Q(s,a)
    step_size = 1/num_sa[state_action]
    td_error = (reward + q_sa_prime - action_val[state_action])
    action_val[state_action] = action_val[state_action] + step_size*td_error*e_trace[state_action]

    # update eligibility trace decayed by λ (aka l)
    e_trace[state_action] = e_trace[state_action]*l
    return action_val[state_action]
#######################################

if __name__ == '__main__':
    main()