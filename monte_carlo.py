
import random
import game
import matplotlib.pyplot as plt
import numpy as np

# Monte-Carlo Control:
#   initialize value fn to 0
#   use time-varying scalar step-size of αt = 1/N(st, at)
#   ε-greedy exploration strategy with et = N0/(N0 + N(st)), 
#       where N0 = 100 is constant (can adjust)
#       N(s) is number of times state s has been visited
#       N(s, a) is number of times that action a has been selected from state s
#   plot optimal value function V*(s) = maxa Q*(s, a) 
#   
#   Plan:
#       Prediction: Use Q(S,A) update formula to find new state-action value for each step in episode
#       Control: Use ε-greedy(Q) to find best Q fn out of set of Q's
#           with prob ε choose action at rand, with prob 1-ε choose greedy


############## Constants ##############
N0 = 40
HIT = "HIT"
STAND = "STAND"
#######################################


################ Logic ################
# game start
def main():
    # num_s = dict storing # of times each state s has been visited; {(int,int):int}
    num_s = {}
    # num_sa = dict storing # of times action a has been taken at state s;
    #   {((int,int),str):int}
    num_sa = {}
    # action_val = dict storing previous Q(s,a) calculated when taking a particular a at particular s
    #   {((int,int),str):int}
    action_val = {}
    cum_reward = 0
    # run n number of episodes
    for i in range(100000):
        # list storing complete history of state-actions and rewards for each episode
        visited = []
        # initial state = tuple(dealer, player)
        state = (game.draw(), game.draw())
        next_a = next_action(state, num_s, num_sa, action_val, visited)

        # while episode has not terminated; step_return = ((current state), reward)
        step_return = None
        while((step_return := game.step(state, next_a))[1] == float('-inf')):
            # state returned after previous execution of game.step
            state = step_return[0]
            next_a = next_action(state, num_s, num_sa, action_val, visited)
            
        # final reward obtained from the terminal state
        reward = step_return[1]

        # after episode terminates, update action_val for each state-action in visited list accordingly
        for state_action in visited:
            # GLIE Monte-Carlo Control Policy Improvement
            q_sa = action_val[state_action]
            action_val[state_action] = q_sa + ((reward - q_sa) / num_sa[state_action])
        # clear visited list
        visited.clear()

        # track cumulative reward across eps; every 100 eps print out
        cum_reward += reward
        if i % 1000 == 0:
            print(f'The cumulative reward at episode {i}: {cum_reward}')

    ############## PLOT ##############
    try:
        # Plot using matplotlib
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # x is dealer, y is player
        _x = np.arange(1,11)
        _y = np.arange(1,22)
        _xx, _yy = np.meshgrid(_x, _y)
        x, y = _xx.ravel(), _yy.ravel()

        # height of bars is equal to the value of the optimal action-val fn of each combination of cards
        top = [max(action_val[(d,p),"HIT"],action_val[(d,p),"STAND"]) for d,p in zip(x, y)]
        bottom = np.zeros_like(top)
        ax.set_zlim(-1, 1)
        width = depth = 1
        ax.bar3d(x, y, bottom, width, depth, top, shade=True)

        ax.set_xticks(_x)
        ax.set_xlabel("Dealer's Hand")
        ax.set_yticks([n for n in _y if n%2==0])
        ax.set_ylabel("Player's Hand")

        plt.show()
    except:
        print("Number of episodes insufficient to train.")
    ##################################


# Updates all relevant data structures for current state-action and returns next action
def next_action(state, num_s, num_sa, action_val, visited):
    # increment and update num_s for this state (meaning visited this state 1 more time)
    num_s.setdefault(state, 0)
    num_s[state] = num_s[state]+1
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
    
    # get action based on existing action-value fn
    visited.append((state, next_a))
    # update num_sa (same concept as updating num_s) with newly obtained action
    num_sa.setdefault((state, next_a), 0)
    num_sa[(state, next_a)] = num_sa[(state, next_a)] + 1
    return next_a
#######################################

if __name__ == '__main__':
    main()