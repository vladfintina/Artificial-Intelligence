#!/usr/bin/env python3
from game.action import *
from game.board import *
from game.artificial_agent import ArtificialAgent
from dead_square_detector import detect
from typing import List, Union, Tuple
import sys
from time import perf_counter
from os.path import dirname
from math import *
# hack for importing from parent package
# de sters inainte de rulare
#from sokoban.game.action import Action, Move, Push
#from sokoban.game.board import EDirection, Board, StateMinimal, ETile

#######################################

sys.path.append(dirname(dirname(dirname(__file__))))
from astar import AStar
from search_templates import HeuristicProblem


class MyAgent(ArtificialAgent):
    """
    Logic implementation for Sokoban ArtificialAgent.

    See ArtificialAgent for details.
    """
    def __init__(self, optimal, verbose) -> None:
        super().__init__(optimal, verbose)  # recommended

    def new_game(self) -> None:
        """Agent got into a new level."""
        super().new_game()  # recommended

    @staticmethod
    def think(
        board: Board, optimal: bool, verbose: bool
    ) -> List[Union[EDirection, Action]]:
        
        """
        Code your custom agent here.
        You should use your A* implementation.

        You can find example implementation (without use of A*)
        in simple_agent.py.
        """
        
        prob = SokobanProblem(board)
        solution = AStar(prob)
        if not solution:
            return None

        return [a.dir for a in solution.actions]


class SokobanProblem(HeuristicProblem):
    """HeuristicProblem wrapper of Sokoban game."""

    def __init__(self, initial_board) -> None:
        # Your implementation goes here.
        # Hint: __init__(self, initial_board) -> None:
        self.initial_board = initial_board
        self.death_squares = detect(initial_board)
        self.height = initial_board.height
        self.width = initial_board.width
        self.coins = []
        self.create_coins_list()
        self.heuristic_distances = [[1000 for _ in range(self.height)] for _ in range(self.width)]
        self.create_matrix_heuristic_distance()

    def create_coins_list(self):
        for i in range(self.width):
            for j in range(self.height):
                t: Tuple = (i, j)
                tile = self.initial_board.tile(t[0], t[1])
                if ETile.is_target(tile):
                    # print(t[0], t[1])
                    self.coins.append(t)

    def calculate_euclidean_distance_(self, x1: int, y1: int, x2: int, y2: int):
        return sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

    def create_matrix_heuristic_distance(self):
        for i in range(self.width):
            for j in range(self.height):
                x1 = i
                y1 = j
                # average_distance = 0
                distance = 0
                min_distance = 10000
                for c in self.coins:
                    x2 = c[0]
                    y2 = c[1]
                    distance = self.calculate_euclidean_distance_(x1, y1, x2, y2)
                    if distance < min_distance:
                        min_distance = distance
                self.heuristic_distances[i][j] = min_distance
                # print(min_distance, end=' ')
            # print()

    def initial_state(self) -> Union[Board, StateMinimal]:
        # Your implementation goes here.
        # Hint: return self.initial_board
        return self.initial_board

    def actions(self, state: Union[Board, StateMinimal]) -> List[Action]:
        # Your implementation goes here.
        actions: List[Action] = []
        for m in Move.get_actions():
            if m.is_possible(state):
                actions.append(m)
        for p in Push.get_actions():
            if p.is_possible(state):
                actions.append(p)
        return actions

    def result(
        self, state: Union[Board, StateMinimal], action: Action
    ) -> Union[Board, StateMinimal]:
        # Your implementation goes here.
        cloneBoard = state.clone()
        action.perform(cloneBoard)
        return cloneBoard

    def is_goal(self, state: Union[Board, StateMinimal]) -> bool:
        # Your implementation goes here.
        return state.is_victory()

    def cost(self, state: Union[Board, StateMinimal], action: Action) -> float:
        # Your implementation goes here.
        return 1

    def estimate(self, state: Union[Board, StateMinimal]) -> float:
        # Your implementation goes here.
        heuristic = 0
        for i in range(self.width):
            for j in range(self.height):
                t: Tuple = (i, j)
                tile = state.tile(t[0], t[1])
                if ETile.is_box(tile):
                    if self.death_squares[i][j]:
                        return 10000000
                    heuristic += self.heuristic_distances[i][j]
        return heuristic
