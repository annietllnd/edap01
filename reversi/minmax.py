"""
def alpha_beta_decision(current_board) -> action:
	
	max = result of maximixing min_value(result(action, current_board))	
return the action in actions[index of action]

#min_value is value is AT MOST 3

----

def max_value(current_board, alpha, beta) -> value:
	if terminal_test(current_board): #if the game is over, return true
		return utility(state)
	v = -inf
	for a, s in successors(current_board)
		v = max(v, min_value(s, alpha, beta))
		if v >= beta: return v
		alpha = max(alpha, v)
	return v
"""

"""
		A
	/		\
B,3				C,2

If we know that B is at most 3, there is no point for MAX to evaluate the successors of 2

Order the moves based on how good they are

max:
if(node < bestMove):
	prune!

initial call:
minimax(currentPosition, 3, -inf, +inf, true)
"""

"""
def valid moves(position, board):
	idx = board.index(position)
	moves = []
	neighbours = [position+i for i in range(1,9)]
	if(position != "green3"):
		return moves
	else:
		for tile in neighbours:
			if(tile = get_opposite_turn(self.turn)):
				moves.append(tile)
		return moves


"""

"""
for position in current_board:
moves = valid_moves(position, current_board)
	minimax(position, depth, alpha, beta, maximixingPlayer)
		if(depth == 0 or terminal_test(position)):
			return eval of position

		if(turn == maximizingPlayer):
			maxEval = -inf
			for valid_move in moves:
				eval = minimax(child, depth-1, alpha, beta, false)
				maxEval = max(maxEval, eval)
				alpha = max(alpha, eval)
				if(beta <= alpha):
					break
			return maxEval
		else:
			minEval = +inf
			for valid_move in moves
				eval = minimax(child, depth-1, alpha, beta, true)
				minEval = min(minEval, eval)
				beta = min(beta, eval)
				if(beta <= alpha):
					break
			return minEval 
"""
