#!/usr/bin/env python3
from game.controllers import PacManControllerBase
from game.pacman import Game, DM, Direction
from typing import List
import sys
from os.path import dirname

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(__file__))))
from search_templates import *
from ucs import ucs


class PacProblem(Problem):
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def initial_state(self) -> int:
        return self.game.pac_loc

    def actions(self, state: int) -> List[int]:
        # possible_actions = self.game.get_possible_pacman_dirs()
        # return possible_actions
        possible_actions = []
        for i in [0, 1, 2, 3]:
            if self.game.get_neighbor(state, i) != -1:
                possible_actions.append(i)
        return possible_actions

    def result(self, state: int, action: int) -> int:
        return self.game.get_neighbor(state, action)

    def is_goal(self, state: int) -> bool:
        someone_edible = False
        # most important goal is to eat edible ghosts if there is any
        for i in [0, 1, 2, 3]:
            if self.game.get_edible_time(i) > 0:
                if self.game.get_ghost_loc(i) == state:
                    return True

        # if there are many ghosts around pac man his goal will be to eat a powerball
        if self.game.get_active_power_pills_count() > 0:
            power_pill_index = self.game.get_power_pill_index(state)
            min_ghost_loc = self.game.get_target(state, self.game.ghost_locs, True, DM.MANHATTAN)
            min_distance = self.game.get_euclidean_distance(state, min_ghost_loc)
            if power_pill_index != -1:
                if self.game.check_power_pill(power_pill_index) and min_distance < 35:
                    return True

        # verifies if there is any edible ghost
        for i in [0, 1, 2, 3]:
            if self.game.is_edible(i):
                someone_edible = True

        # if there is a fruit in the game and no ghost edible the fruit will be the only goal possible
        if self.game.fruit_loc > 0 and not someone_edible:
            if self.game.fruit_loc == state:
                return True
            else:
                return False
        # verifies if the state is a pill and no one is edible, if so it is declared as a goal
        pill_index = self.game.get_pill_index(state)
        if pill_index != -1 and not someone_edible:
            if self.game.check_pill(pill_index):
                return True

        return False

    def cost(self, state: int, action: int) -> float:
        for i in [0, 1, 2, 3]:
            if not self.game.is_edible(i):
                if self.game.get_ghost_loc(i) == state:
                    return 10000000

        for i in [0, 1, 2, 3]:
            if self.game.is_edible(i):
                if self.game.get_ghost_loc(i) == state:
                    return 1

        for i in [0, 1, 2, 3]:
            ghost_loc = self.game.get_ghost_loc(i)
            manhattan_dist = self.game.get_manhattan_distance(state, ghost_loc)
            euclidean_dist = self.game.get_euclidean_distance(state, ghost_loc)
            # print(manhattan_dist)
            if euclidean_dist < 25 and not self.game.is_edible(i):
                return 10000

        if self.game.fruit_loc == state:
            return 30

        if self.game.get_active_power_pills_count() > 0:
            power_pill_index = self.game.get_power_pill_index(state)
            min_ghost_loc = self.game.get_target(state, self.game.ghost_locs, True, DM.MANHATTAN)
            min_distance = self.game.get_euclidean_distance(state, min_ghost_loc)
            if power_pill_index != -1:
                if self.game.check_power_pill(power_pill_index) and min_distance < 30:
                    return 10
                else:
                    return 1000000

        return 100


class Agent_Using_UCS(PacManControllerBase):
    def tick(self, game: Game) -> None:
        prob = PacProblem(game)
        sol = ucs(prob)
        if sol is None or not sol.actions:
            pass
            # if self.verbose:
            #     print("No path found.", file=sys.stderr)
        else:
            self.pacman.set(sol.actions[0])
