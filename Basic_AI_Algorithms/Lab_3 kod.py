import random as rand
import time

# 0 = puste
# 1 = cross (max) first player
# 2 = circle (min)

# game configuration
N = 3
M = 3
k = 3

# state evaluation vector
H = [3,2,3,2,4,2,3,2,3]

# list of winnig terminal states 
T = [
    [1,1,1,0,0,0,0,0,0],
    [0,0,0,1,1,1,0,0,0],
    [0,0,0,0,0,0,1,1,1],
    [1,0,0,1,0,0,1,0,0],
    [0,1,0,0,1,0,0,1,0],
    [0,0,1,0,0,1,0,0,1],
    [1,0,0,0,1,0,0,0,1],
    [0,0,1,0,1,0,1,0,0]
]

# index in state array
player = M*N
value = M*N+1


def game(pl1_cfg, pl2_cfg):
    pl1_d = pl1_cfg[0]
    pl1_ab = pl1_cfg[1]
    pl2_d = pl2_cfg[0]
    pl2_ab = pl2_cfg[1]
    current_state = [0,0,0,0,0,0,0,0,0,1,0]
    pl1_states = 0
    pl2_states = 0
    while(True):
        if pl1_ab == True:
            new_state, new_states = alfabeta_player(current_state, pl1_d)
            pl1_states += new_states
            current_state = new_state
        else:
            new_state, new_states = minimax_player(current_state, pl1_d)
            pl1_states += new_states
            current_state = new_state
        if current_state[value] == 100:
            return 1, pl1_states, pl2_states
        elif (if_draw_terminal(current_state)):
            return 0, pl1_states, pl2_states
        if pl2_ab == True:
            new_state, new_states = alfabeta_player(current_state, pl2_d)
            pl2_states += new_states
            current_state = new_state
        else:
            new_state, new_states = minimax_player(current_state, pl2_d)
            pl2_states += new_states
            current_state = new_state
        if current_state[value] == -100:
            return 2, pl1_states, pl2_states
        elif (if_draw_terminal(current_state)):
            return 0, pl1_states, pl2_states


def game_random(pl1_d):
    current_state = [0,0,0,0,0,0,0,0,0,1,0]
    while(True):
        new_state, new_states = alfabeta_player(current_state, pl1_d)
        current_state = new_state
        if current_state[value] == 100:
            return 1
        elif (if_draw_terminal(current_state)):
            return 0
        new_state = random_player(current_state)
        current_state = new_state
        if current_state[value] == -100:
            return 2
        elif (if_draw_terminal(current_state)):
            return 0


# returns possible successors of the given state
def successors(state):
    successors_list = []
    new_value = state[player]
    for i in range(N*M):
        if state[i] == 0:
            state_new = state.copy()
            if state[player] == 1:
                state_new[player] = 2
            else:
                state_new[player] = 1 
            state_new[i] = new_value
            successors_list.append(state_new)
    return successors_list


# returns an evaluation of the given state
def heuristic_function(state):
    sum_max = 0
    sum_min = 0
    for i in range(N*M):
        if state[i] == 1:
            sum_max += H[i]
        elif state[i] == 2:
            sum_min += H[i]
    return sum_max - sum_min


def if_winning_terminal(state):
    current_player_value = state[player]
    for t in T:
        for i in range(N*M):
            if t[i] == 1:
                if state[i] == current_player_value or state[i] == 0:
                    break
        else:
            return True    
    return False


def if_draw_terminal(state):
    for i in range(M*N):
        if state[i] == 0:
            return False
    else:
        return True


def find_max_state(states):
    best_state = states[0]
    best_value = states[0][value]
    for state in states:
        if state[value] > best_value:
            best_value = state[value]
            best_state = state
    return best_state


def find_min_state(states):
    best_state = states[0]
    best_value = states[0][value]
    for state in states:
        if state[value] < best_value:
            best_value = state[value]
            best_state = state
    return best_state


def minimax(state, d):
    estimated_states = 0
    if if_winning_terminal(state):
        if state[player] == 2:
            return 100, estimated_states
        else:
            return -100, estimated_states
    elif if_draw_terminal(state):
        return 0, estimated_states
    elif d == 0:
        return heuristic_function(state), estimated_states
    U = successors(state)
    estimated_states += len(U)
    w = []
    for u in U:
        new_w, new_states = minimax(u, d-1)
        estimated_states += new_states
        w.append(new_w)
    if state[player] == 1:
        return max(w), estimated_states
    elif state[player] == 2:
        return min(w), estimated_states


def minimax_player(state, d):
    U = successors(state)
    w = []
    estimated_states = len(U)
    for u in U:
        new_value, new_states = minimax(u, d-1)
        estimated_states += new_states
        u[value] = new_value
        w.append(u)
    if state[player] == 1:
        return find_max_state(w), estimated_states
    elif state[player] == 2:
        return find_min_state(w), estimated_states


def alfabeta(state, d, alfa, beta):
    estimated_states = 0
    if if_winning_terminal(state):
        if state[player] == 2:
            return 100, estimated_states
        else:
            return -100, estimated_states
    elif if_draw_terminal(state):
        return 0, estimated_states
    elif d == 0:
        return heuristic_function(state), estimated_states
    U = successors(state)
    estimated_states += len(U)
    if state[player] == 1:
        for u in U:
            new_alfa, new_states = alfabeta(u, d-1, alfa, beta)
            estimated_states += new_states
            alfa = max(alfa, new_alfa)
            if alfa >= beta:
                return beta, estimated_states
        return alfa, estimated_states
    elif state[player] == 2:
        for u in U:
            new_beta, new_states = alfabeta(u, d-1, alfa, beta)
            estimated_states += new_states
            beta = min(beta, new_beta)
            if alfa >= beta:
                return alfa, estimated_states
        return beta, estimated_states
    
def alfabeta_player(state, d):
    U = successors(state)
    estimated_states = len(U)
    w = []
    for u in U:
        new_value, new_states = alfabeta(u, d-1, -999, 999)
        estimated_states += new_states
        u[value] = new_value
        w.append(u)
    if state[player] == 1:
        return find_max_state(w), estimated_states
    elif state[player] == 2:
        return find_min_state(w), estimated_states


def random_player(state):
    U = successors(state)
    choice = rand.choice(U)
    if if_winning_terminal(choice):
        choice[value] = -100
        return choice
    elif if_draw_terminal(choice):
        choice[value] = 0
        return choice
    return rand.choice(U)


if __name__ == "__main__":
    option = 2
    if option == 1:
        wins = 0
        draws = 0
        loses = 0
        for i in range(1000):
            result = game_random(5)
            if result == 0:
                draws += 1
            elif result == 1:
                wins += 1
            else:
                loses += 1
        print("Wins: " + str(wins))
        print("Draws: " + str(draws))
        print("Loses: " + str(loses))
    elif option == 2:
        print(game([9, True], [4, True]))