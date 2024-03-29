import pygame
import os
from Setting import board_position
from math import pow


class King:
    # 0 for red side; 1 for black side
    img = [pygame.image.load(os.path.join('imgs', 'king.png')),
           pygame.image.load(os.path.join('imgs', 'king_g.png'))]

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

    def show_legal_move(self, teammate_loc, opponent_loc, kings):
        # This piece can only move one step(up,down,left,right) inside its 2x2 square
        legal_move, remove = [], []

        legal_move.append([self.x, self.y - 1])     # up
        legal_move.append([self.x, self.y + 1])     # down
        legal_move.append([self.x - 1, self.y])     # left
        legal_move.append([self.x + 1, self.y])     # right

        for move in legal_move:
            # check x
            if move[0] < 3 or move[0] > 5 \
                    or move in teammate_loc:
                remove.append(move)
            else:  # check y
                if self.color == 0:
                    if move[1] < 0 or move[1] > 2:
                        remove.append(move)
                elif self.color == 1:
                    if move[1] < 7 or move[1] > 9:
                        remove.append(move)

        king_eat_king = 0
        if kings[0].x == kings[1].x:    # if both kings on same x coordinate
            for y in range(kings[0].y+1, kings[1].y):
                # if there exists any pieces between two kings
                if [self.x, y] in teammate_loc or [self.x, y] in opponent_loc:
                    king_eat_king += 1      # add 1 if pieces between two kings exists

        # if no pieces between two kings and two kings on same x axis, you can use your king to eat opponent king
        if king_eat_king == 0:
            legal_move.append([kings[1 - self.color].x, kings[1 - self.color].y])

        for el in remove:
            legal_move.remove(el)

        return legal_move

    def update_coordinate(self, x, y):
        self.x = x
        self.y = y
        self.rect[0] = board_position[self.y][self.x][0]
        self.rect[1] = board_position[self.y][self.x][1]
