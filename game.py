import random
import monte_carlo as mc

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
    next_action = mc.next_action(next_state)
    return step(next_state, next_action)