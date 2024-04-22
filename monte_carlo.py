
import random

# Monte-Carlo Control:
#   initialize value fn to 0
#   use time-varying scalar step-size of αt = 1/N(st, at)
#   e-greedy exploration strategy with et = N0/(N0 + N(st)), 
#       where N0 = 100 is constant (can adjust)
#       N(s) is number of times state s has been visited
#       N(s, a) is number of times that action a has been selected from state s
#   plot optimal value function V*(s) = maxa Q*(s, a) 
#   
#   Plan:
#       Prediction: Use Q(S,A) update formula to find new state-action value for each step in episode
#       Control: Use e-greedy(Q) to find best Q fn out of set of Q's
#           with prob e choose action at rand, with prob 1-e choose greedy


############## Constants ##############
N0 = 40
HIT = "HIT"
STAND = "STAND"
#######################################


############### Globals ###############
# num_s = dict storing # of times each state s has been visited; {(int,int):int}
num_s = {}
# num_sa = dict storing # of times action a has been taken at state s;
#   {((int,int),str):int}
num_sa = {}
# action_val = dict storing previous Q(s,a) calculated when taking a particular a at particular s
#   {((int,int),str):int}
action_val = {}
# global list variable storing history of state-actions per episode
visited = []
#######################################


################ Logic ################
# game start
def main():
    cum_reward = 0
    # run 10000 episodes
    for i in range(100000):
        # initial state = tuple(dealer, player)
        initial_state = (random.randint(1, 10), random.randint(1, 10))
        # get action based on existing action-value fn
        action = next_action(initial_state)
        # get reward for this episode. synonymous with return here due to no discounting
        reward = step(initial_state, action)

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
            print(action_val)
            #print(f'The cumulative reward at episode {i}: {cum_reward}')


# returns next action
def next_action(state):
    # increment and update num_s for this state (meaning visited this state 1 more time)
    if state not in num_s:
        num_s[state] = 0
    num_s[state] = num_s[state]+1
    #num_s.setdefault(state, 0)
    #num_s[state] = num_s[state]+1

    # initialize action_val to 0 for both hit and stand for this state if not existing
    action_val.setdefault((state, HIT), 0)
    action_val.setdefault((state, STAND), 0)

    # e-greedy exploration with et = N0/(N0 + N(st))
    epsilon = N0 / (N0 + num_s[state])

    # Control: Use e-greedy(Q) to find best Q fn out of set of Q's;
    #   With prob epsilon choose action at rand, with prob 1-e choose greedy
    action = ''
    if random.random() <= epsilon or action_val[(state, HIT)] == action_val[(state, STAND)]:
        action = random.choice([HIT, STAND])
    else:
        action = HIT if action_val[(state, HIT)] > action_val[(state, STAND)] else STAND
    
    # update num_sa (same concept as updating num_s)
    num_sa.setdefault((state, action), 0)
    num_sa[(state, action)] = num_sa[(state, action)] + 1

    # append each visited state-action to visited
    visited.append((state, action))

    # finally return action to take
    return action


# Parameters: 
#   state (dealer's first card 1-10 and the player's sum 1-21)
#   action (hit or stand)
# Returns: 
#   sample of the next state s' (may be terminal if game finished)
#   AND reward r
def step(state, action):

    # state is a tuple
    dealer = state[0]
    player = state[1]

    # if previous action was stand
    if action == "STAND":
        while(dealer < 17 and dealer >= 1):
            # calculating dealer's next card. must first pick random card 1-10
            dealer_next = random.randint(1, 10)
            # then determine if it is red (1/3) or black (2/3)
            dealer_next = dealer_next*-1 if random.randint(1,3) == 1 else dealer_next
            dealer += dealer_next

        # if dealer busts
        if dealer < 1 or dealer > 21:
            return 1
        
        # if dealer doesn't bust, higher sum wins
        if dealer < player: return 1
        elif dealer > player: return -1
        else: return 0
    
    # if previous action was hit
    elif action == "HIT":
        player_next = random.randint(1,10)
        player_next = player_next*-1 if random.randint(1,3) == 1 else player_next
        player += player_next

        # if player busts
        if player < 1 or player > 21:
            return -1
        
    # if previous action was hit, continue the game; ask RL model for next action
    next_state = (dealer, player)
    nxt_action = next_action(next_state)
    return step(next_state, nxt_action)

#######################################

if __name__ == '__main__':
    main()