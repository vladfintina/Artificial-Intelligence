#!/usr/bin/env python3

from game.board import Board, ETile, EDirection
from typing import List, Tuple
import heapq
from heapq import heappush, heappop


def detect(board: Board) -> List[List[bool]]:
    """
    Returns 2D matrix containing true for dead squares.

    Dead squares are squares, from which a box cannot possibly
     be pushed to any goal (even if Sokoban could teleport
     to any location and there was only one box).

    You should prune the search at any point
     where a box is pushed to a dead square.

    Returned data structure is
        [board_width] lists
            of [board_height] lists
                of bool values.
    (This structure can be indexed "struct[x][y]"
     to get value on position (x, y).)
    """
    dead_Squares = [[True for _ in range(board.height)] for _ in range(board.width)]
    cBoard = board.clone()
    tiles = cBoard.tiles
    targets = []
    height = cBoard.height
    width = cBoard.width
    for i in range(width):
        for j in range(height):
            t: Tuple = (i, j)
            tile = cBoard.tile(t[0], t[1])
            if ETile.is_target(tile):
                targets.append(t)
                dead_Squares[t[0]][t[1]] = False

    queue: heapq = []
    for target in targets:
        heappush(queue, target)
        while queue.__len__() > 0:
            tile = heappop(queue)
            for direction in EDirection:
                if dead_Squares[tile[0] + direction.dx][tile[1] + direction.dy]:
                    cBoard.relocate_sokoban(tile[0], tile[1])
                    stile1 = cBoard.stile(direction)
                    if not ETile.is_wall(stile1):
                        cBoard.relocate_sokoban(tile[0] + direction.dx, tile[1] + direction.dy)
                        stile2 = cBoard.stile(direction)
                        if not ETile.is_wall(stile2):
                            heappush(queue, (tile[0] + direction.dx, tile[1] + direction.dy))
                            dead_Squares[tile[0] + direction.dx][tile[1] + direction.dy] = False

    return dead_Squares


