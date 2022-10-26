'''
Name(s): Ethan Honey, Sidharth Daga
UW netid(s): ehoney22, sidaga
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.prune = True
        self.num_states = 0
        self.ab_cutoffs = 0
        self.maxply = 2
        self.static_eval = self.staticEval
        # feel free to create more instance variables as needed.

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "ehoney22 sidaga"

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        # TODO: use the prune flag to indiciate what search alg to use
        self.prune = prune
        self.num_states = 0
        self.ab_cutoffs = 0

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # TODO: return a tuple containig states and cutoff
        return (self.num_states, self.ab_cutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        if func is not None:
            self.static_eval = func
        else:
            self.static_eval = self.staticEval

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        currentPly = 1
        who = state.whose_move
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)
        moves = self.get_all_possible_moves()
        best_move = None
        best_score = float("-inf")
        if self.prune:
            for move in moves:
                temp_score = BackgammonPlayer.ab_helper(self, move[1], currentPly, who, die1, die2, float("-inf"), float("+inf"))
                if temp_score > best_score:
                    best_score = temp_score
                    best_move = move[0]
        else:
            for move in moves:
                temp_score = BackgammonPlayer.move_helper(self, move[1], currentPly, who, die1, die2)
                if temp_score > best_score:
                    best_score = temp_score
                    best_move = move[0]
        return best_move

    def move_helper(self, state, currentPly, who, die1, die2):
        self.num_states += 1
        if (currentPly == self.maxply):
            return self.static_eval(state)
        else:
            self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)
            moves = self.get_all_possible_moves()
            if who == 0:
                return max([BackgammonPlayer.move_helper(self, move[1], currentPly+1, 1-who, die1, die2) for move in moves])
            elif who == 1:
                return min([BackgammonPlayer.move_helper(self, move[1], currentPly+1, 1-who, die1, die2) for move in moves])

    def ab_helper(self, state, currentPly, who, die1, die2, alpha, beta):
        self.num_states += 1
        if currentPly == self.maxply:
            return self.static_eval(state)
        else:
            self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)
            moves = self.get_all_possible_moves()
            v = None
            if (who == 0):
                for move in moves:
                    v = BackgammonPlayer.ab_helper(self, move[1], currentPly+1, 1-who, die1, die2, alpha, beta)
                    if v > alpha:
                        alpha = v
                    if alpha >= beta:
                        self.ab_cutoffs += 1
                        return alpha
            else:
                for move in moves:
                    v = BackgammonPlayer.ab_helper(self, move[1], currentPly+1, 1-who, die1, die2, alpha, beta)
                    if v < beta:
                        beta = v
                    if alpha >= beta:
                        self.ab_cutoffs += 1
                        return beta
            return v

    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves. Returns an array of move commands"""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        pass_state = None
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m)    # Add the move to the list.
                elif m[0] == 'p':
                    pass_state = m[1]
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append(('p', pass_state))
        return move_list


    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state
        count = len(state.white_off)*1000 - len(state.red_off)*1000
        whitepip = 0
        redpip = 0
        whitesolo = 0
        redsolo = 0
        for i in range(len(state.pointLists)):
            for j in range(len(state.pointLists[i])):
                if state.pointLists[i][j] == 0:
                    whitepip += (24 - i)
                    if len(state.pointLists[i]) == 1:
                           whitesolo += 1
                else:
                    redpip += i
                    if len(state.pointLists[i]) == 1:
                           redsolo += 1
        count += (redpip-whitepip)*10
        count -= whitesolo*10
        count += redsolo*10
        if (len(state.bar) > 0):
            if state.bar[0] == 0:
                count -= 500 * len(state.bar)
            else:
                count += 500 * len(state.bar)
        return count
        
