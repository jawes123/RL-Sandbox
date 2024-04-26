import random

# Parameters: 
#   state (dealer's first card 1-10 and the player's sum 1-21)
#   action (hit or stand)
# Returns: 
#   sample of the next state s' AND reward r
#   ((current state), reward)
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

        # if dealer busts or has higher sum than player
        if dealer < 1 or dealer > 21 or dealer < player:
            reward = 1
        # if player has higher sum
        elif dealer > player: reward = -1
        # if sums are same, draw
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


def draw():
    return random.randint(1, 10)