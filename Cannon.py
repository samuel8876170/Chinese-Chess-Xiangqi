import pygame
import os
from Setting import board_position


class Cannon:
    # 0 for red side; 1 for black side
    img = [pygame.image.load(os.path.join('imgs', 'boom.png')),
           pygame.image.load(os.path.join('imgs', 'boom_g.png'))]

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        # (top_left x-y, bottom_right x-y)
        self.rect = [board_position[self.y][self.x][0], board_position[self.y][self.x][1],
                     self.img[0].get_width(), self.img[0].get_height()]

    def draw(self, win):
        win.blit(self.img[self.color], board_position[self.y][self.x])
        pygame.draw.rect(win, (255, 0, 0), self.rect, 1)
        pygame.display.update()

    # This will give us all legal move -> no.row, no.column
    def show_legal_move(self, teammate_loc, opponent_loc):
        # This piece can only move to its [up,down,left,right] side
        legal_move = []
        for move_x in range(9):
            legal_move.append([move_x, self.y])
        for move_y in range(10):
            legal_move.append([self.x, move_y])

        legal_move.remove([self.x, self.y])
        legal_move.remove([self.x, self.y])

        remove = []
        # special deletion for each pieces
        for move in legal_move:  # do not delete the rect of opponent as we want the piece eat it
            for location in teammate_loc:        # consider teammate collision with path
                if location in legal_move:
                    if move[0] <= location[0] < self.x or self.x < location[0] <= move[0]\
                            or move[1] <= location[1] < self.y or self.y < location[1] <= move[1]:
                        remove.append(move)

            for location in opponent_loc:        # consider opponent collision with path
                if location in legal_move:
                    if move[0] <= location[0] < self.x or self.x < location[0] <= move[0] \
                            or move[1] <= location[1] < self.y or self.y < location[1] <= move[1]:
                        remove.append(move)

        non_repeated, obstacles = [], []  # teammate_group, opponent_group

        for element in remove:             # delete redundant repeated legal_move
            if element not in non_repeated:
                non_repeated.append(element)

        for el in non_repeated:
            legal_move.remove(el)
            if el in opponent_loc or el in teammate_loc:
                obstacles.append(el)

        sides = [[], [], [], []]    # left, right, up, down
        # separate opponent location in to different side
        for loc in obstacles:
            if loc[0] < self.x:     # left
                sides[0].append(loc)
            elif loc[0] > self.x:   # right
                sides[1].append(loc)
            elif loc[1] < self.y:   # up
                sides[2].append(loc)
            elif loc[1] > self.y:   # down
                sides[3].append(loc)

        # sort each location by distance between loc and self
        # choose the second opponent_location and append it into legal_move,if this is opponent.
        # then we can choose that hit-box to activate 'eat' function
        for side in sides:
            distance = []
            for loc in side:
                distance.append(abs((self.x - loc[0]) + (self.y - loc[1])))

            # sort by distance
            for i in range(len(distance)):
                for j in range(i, len(distance)):
                    if distance[i] > distance[j]:
                        # switch distance
                        temp_dis = distance[i]
                        distance[i] = distance[j]
                        distance[j] = temp_dis
                        # switch loc(x,y)
                        temp_loc = side[i]
                        side[i] = side[j]
                        side[j] = temp_loc

        for side in sides:
            if len(side) >= 2:
                if side[1] in opponent_loc:
                    legal_move.append(side[1])

        return legal_move

    def update_coordinate(self, x, y):
        self.x = x
        self.y = y
        self.rect[0] = board_position[self.y][self.x][0]
        self.rect[1] = board_position[self.y][self.x][1]
