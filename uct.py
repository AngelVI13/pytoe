import random
import time
from multiprocessing import Queue, Process
from operator import itemgetter

from board import Board
from node import Node


def uct_multi(rootstate_: Board, itermax):
    moves = rootstate_.get_moves()

    if len(moves) == 1:  # if only 1 move is possible don't bother searching anything
        return moves[0]

    avg_iters = itermax // len(moves)
    queue = Queue()

    # processes = []
    # for move in moves:
    #     current_state = rootstate_.__copy__()
    #     current_state.make_move(move)
    #     p = Process(target=uct, args=(queue, move, current_state, avg_iters))
    #     p.start()
    #     processes.append(p)
    #
    # for process in processes:
    #     process.join()
    for move in moves:
        state = rootstate_.__copy__()
        state.make_move(move)
        # Check for immediate result after this make_move()
        # It is possible the game is already over by this point in which the value of the move should
        # be immediately computed and put in the result from the vue point of the enemy
        # since later moves are evaluated from that viewpoint
        result = state.get_result(-state.playerJustMoved)
        if result is not None:
            queue.put((move, result, 1))
            continue  # here 1 referes to number of visits
        uct(queue, move, state, avg_iters)
    time.sleep(0.1)

    results = []
    while not queue.empty():
        move, wins, visits = queue.get()
        print(f'Move: {move}, score: {wins/visits}, visits: {visits} from {avg_iters}')
        results.append((move, wins/visits))

    # the score here refers to the score of the best enemy reply -> we choose a move which leads to a best enemy reply
    # with the least score
    best_move, score = sorted(results, key=itemgetter(1))[0]
    return best_move


def rand_choice(x):  # fastest way to get random item from list
    return x[int(random.random() * len(x))]


def uct(queue: Queue, move_origin, rootstate, itermax):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    state = rootstate
    for i in range(itermax):
        node = rootnode
        moves_to_root = 0

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.uct_select_child()
            state.make_move(node.move)
            moves_to_root += 1

        # Expand
        if node.untriedMoves:  # if we can expand (i.e. state/node is non-terminal)
            m = rand_choice(node.untriedMoves)
            state.make_move(m)
            moves_to_root += 1
            node = node.add_child(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_result(state.playerJustMoved) is None:  # while state is non-terminal
            state.make_move(rand_choice(state.get_moves()))
            moves_to_root += 1

        # Backpropagate
        while node is not None:  # backpropagate from the expanded node and work back to the root node
            # state is terminal. Update node with result from POV of node.playerJustMoved
            result = state.get_result(node.playerJustMoved)
            node.update(result)
            node = node.parentNode

        for _ in range(moves_to_root):
            state.take_move()

    best_node = sorted(rootnode.childNodes, key=lambda c: c.visits)[-1]
    queue.put((move_origin, best_node.wins, best_node.visits))


if __name__ == '__main__':
    b = Board()
    print(uct_multi(b, itermax=20))
