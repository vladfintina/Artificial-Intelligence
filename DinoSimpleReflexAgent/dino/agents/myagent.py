#!/usr/bin/env python3
from game.dino import *
from game.agent import Agent


class MyAgent(Agent):
    """Reflex agent static class for Dino game."""

    @staticmethod
    def is_on_the_ground(game):
        if game.dino.y == game.dino.Y or game.dino.y == game.dino.Y_DUCK:
            return True
        return False

    @staticmethod
    def obstacle_ignore(game: Game, o: Obstacle) -> bool:
        if o.rect.bottom < game.dino.Y:
            return True
        return False

    @staticmethod
    def is_before_obstacle(game: Game, obst: Obstacle):
        dino = game.dino
        if dino.x < obst.rect.x:
            return True
        return False

    @staticmethod
    def is_close_enough(game: Game, o: Obstacle):
        if o.rect.coords.x < game.dino.x + 115 + 5 * (
                game.speed - 5):
            return True
        return False

    @staticmethod
    def simple_jump(game: Game, obst: Obstacle) -> bool:
        if obst.rect.bottom == game.GROUND_Y or (obst.rect.y + obst.rect.height) >= game.dino.Y_DUCK:
            return True
        return False

    @staticmethod
    def can_move_right_over_object_after_jump(game: Game, obst: Obstacle) -> bool:
        dino = game.dino
        obst = obst.rect
        speed_constant = game.speed * 1000
        if dino.y + dino.body.height + dino.head.height <= obst.y\
                and obst.x - 200 <= dino.x <= obst.x + obst.width / (speed_constant * (game.speed/3)):  # dino.x <= obst.x + obst.width / (speed_constant * (game.speed/6)):
            return True
        return False

    @staticmethod
    def safe_to_get_DOWN_RIGHT_after_object(game: Game, obst: Obstacle) -> bool:
        dino = game.dino
        obst = obst.rect
        speed_constant = game.speed * 1000
        if dino.y + dino.body.height + dino.head.height <= obst.y\
                and obst.x + obst.width / (speed_constant * (game.speed/3)) <= dino.x < (obst.x + obst.width):
            return True
        return False

    @staticmethod
    def safe_to_get_DOWN_after_object(game: Game, obst: Obstacle) -> bool:
        dino = game.dino
        obst = obst.rect
        if dino.y + dino.body.height + dino.head.height <= obst.y and dino.x >= obst.x + obst.width:
                #or (dino.x >= obst.x + obst.width and
                #MyAgent.is_on_the_ground(game).__eq__(False)):
            return True
        return False

    @staticmethod
    def simple_duck(game: Game, obst: Obstacle) -> bool:
        if game.dino.Y_DUCK > (obst.rect.y + obst.rect.height) > game.dino.Y:
            return True
        return False

    @staticmethod
    def must_stay_down(game: Game, obst: Obstacle) -> bool:
        if game.dino.head.x <= (obst.rect.x + obst.rect.width):
            return True
        return False

    @staticmethod
    def distance_between_objects(obst1: Obstacle, obst2: Obstacle):
        return obst2.rect.x - obst1.rect.x

    @staticmethod
    def cant_make_down_in_time(game: Game, distance: int, currentObs: Obstacle, nextObs: Obstacle) -> bool:
        # print( currentObs.rect.x, " < ", game.dino.x, " < ", nextObs.rect.x)
        # print("d: ", distance)
        if not MyAgent.is_on_the_ground(game) \
                and currentObs.rect.x < game.dino.x < nextObs.rect.right \
                and (0 < distance < (game.speed + 1) * (game.speed + 1) or 0 < distance < 150) \
                and not MyAgent.obstacle_ignore(game, nextObs):
            # print("d: ", distance, " s: ", game.speed)
            # print("o: ", currentObs.type)
            # print(game.dino.x)
            return True
        # if not MyAgent.still_on_the_ground(game) \
        #        and not MyAgent.is_close_enouqh(game, currentObs):
        #    print("d: ", distance, " s: ", game.speed)
        #    return True
        return False


    @staticmethod
    def get_move(game: Game) -> DinoMove:
        """
        Note: Remember you are creating simple-reflex agent, that should not
        store or access any information except provided.
        """
        # # for visual debugging intellisense you can use
        # from game.debug_game import DebugGame
        # game: DebugGame = game
        # t = game.add_text(Coords(10, 10), "red", "Text")
        # t.text = "Hello World"
        # game.add_dino_rect(Coords(-10, -10), 150, 150, "yellow")
        # l = game.add_dino_line(Coords(0, 0), Coords(100, 0), "black")
        # l.dxdy.update(50, 30)
        # l.dxdy.x += 50
        # game.add_moving_line(Coords(1000, 100), Coords(1000, 500), "purple")

        # YOUR CODE GOES HERE
        for o in game.obstacles:
            #print(o.type)
            #print(game.PREVIOUS_OBSTACLE)
           # distance_between_obstacles = MyAgent.distance_between_objects(o, game.previous_obstacle)
            #print(game.speed)

            if MyAgent.is_close_enough(game, o):
                if MyAgent.simple_duck(game, o) and MyAgent.must_stay_down(game, o):
                    #print("Down_duck")
                    return DinoMove.DOWN

            if game.obstacles.__len__() >= 2:
                # print("o2--", game.obstacles._getitem_(0).type)
                # print("o1--", o.type)
                # print("d: ", distance)
                currentObs = game.obstacles.__getitem__(game.obstacles.__len__() - 1)
                nextObs = game.obstacles.__getitem__(game.obstacles.__len__() - 2)
                distance = nextObs.rect.x - currentObs.rect.right
                # print("d: ", distance, " s: ", game.speed)
                if MyAgent.cant_make_down_in_time(game, distance, currentObs, nextObs):
                    # print("stay up")
                    return DinoMove.RIGHT

            if MyAgent.is_close_enough(game, o):
                if MyAgent.is_on_the_ground(game) and MyAgent.is_before_obstacle(game, o):
                    if MyAgent.simple_jump(game, o):
                        #print("Jump")
                        return DinoMove.UP
                if MyAgent.can_move_right_over_object_after_jump(game, o):
                    #print("Right")
                    return DinoMove.RIGHT
                if MyAgent.safe_to_get_DOWN_RIGHT_after_object(game, o):
                    #print("Down_right_from_jump")
                    return DinoMove.DOWN_RIGHT
                if MyAgent.safe_to_get_DOWN_after_object(game, o):
                    #print("Down_from_jump")
                    return DinoMove.DOWN

        return DinoMove.NO_MOVE


