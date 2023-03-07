#!/usr/bin/env python3
import heapq

from search_templates import Solution, HeuristicProblem
from dataclasses import dataclass, field

@dataclass(order=True)
class Node:
    state: object = field(compare=False)
    action: object = field(compare=False)
    parent: "Node" = field(compare=False)
    cost: float = field(compare=False)
    depth: int = field(compare=False)
    heuristic_cost: float #= field(compare=False)

    def get_state(self) -> object:
        return self.state

    def get_action(self) -> object:
        return self.action

    def get_parent(self) -> "Node":
        return self.parent

    def get_cost(self) -> float:
        return self.cost

    def get_depth(self) -> int:
        return self.depth

    def get_heuristic_cost(self) -> float:
        return self.heuristic_cost

    def existing_node(self, other_state: object):
        if other_state == self.state:
            return True
        return False


def get_path(current_node) -> list:
    path = []
    while current_node.get_parent() is not None:
        path.insert(0, current_node.get_action())
        current_node = current_node.get_parent()
    return path


def AStar(prob: HeuristicProblem) -> Solution:
    """Return Solution of the problem solved by AStar search."""
    init_state = prob.initial_state()
    root = Node(init_state, None, None, 0, 0, 0)

    frontier: heapq = []
    heapq.heappush(frontier, root)

    visited = set()
    i = 0
    while frontier.__len__() != 0:
        #print(i)
        i= i+1
        current_node: Node = heapq.heappop(frontier)
        current_state = current_node.get_state()
        if current_state not in visited:
            visited.add(current_state)
            current_cost = current_node.get_cost()
            # print(current_state)

            if prob.is_goal(current_state):
                path = get_path(current_node)
                return Solution(path, current_state, current_cost)

            for action in prob.actions(current_state):
                new_state = prob.result(current_state, action)
                new_cost = current_cost + prob.cost(current_state, action)
                new_state_estimation = new_cost + prob.estimate(new_state)
                new_node = Node(new_state, action, current_node, new_cost, current_node.get_depth() + 1, new_state_estimation)
                heapq.heappush(frontier, new_node)

    return None
    # return Solution([actions leading to goal], goal_state, path_cost)
