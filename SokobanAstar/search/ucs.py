#!/usr/bin/env python3
import heapq
import sys
from dataclasses import dataclass, field

from search_templates import Problem, Solution
from typing import Optional


@dataclass(order=True)
class Node:
    state: object = field(compare=False)
    action: object = field(compare=False)
    parent: "Node" = field(compare=False)
    cost: float
    depth: int = field(compare=False)

    def get_state(self) -> object:
        return self.state

    def get_action(self) ->object:
        return self.action

    def get_parent(self) -> "Node":
        return self.parent

    def get_cost(self) -> float:
        return self.cost

    def get_depth(self) -> int:
        return self.depth


def get_path(current_node) -> list:
    path = []
    while current_node.get_parent() is not None:
        path.insert(0, current_node.get_action())
        current_node = current_node.get_parent()
    return path


def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by UCS search."""
    # Your implementation goes here.
    init_state = prob.initial_state()
    root = Node(init_state, None, None, 0, 0)

    frontier: heapq = []
    heapq.heappush(frontier, root)

    visited = set()

    while frontier.__len__() != 0:
        current_node: Node = heapq.heappop(frontier)
        current_state = current_node.get_state()
        if current_state not in visited:
            visited.add(current_state)
            current_cost = current_node.get_cost()

            if prob.is_goal(current_state):
                path = get_path(current_node)
                return Solution(path, current_state, current_node.get_cost())

            for action in prob.actions(current_state):
                new_state = prob.result(current_state, action)
                new_cost = current_cost + prob.cost(current_state, action)
                new_node = Node(new_state, action, current_node, new_cost, current_node.get_depth() + 1)
                heapq.heappush(frontier, new_node)

    return None
    # raise NotImplementedError

    # return Solution([actions leading to goal], goal_state, path_cost)
