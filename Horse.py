import pygame
import os
from Setting import board_position


class Horse:
    # 0 for red side; 1 for black side
    img = [pygame.image.load(os.path.join('imgs', 'horse.png')),
           pygame.image.load(os.path.join('imgs', 'horse_g.png'))]

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

    def show_legal_move(self, teammate_loc, opponent_loc):
        # This piece can only move as a (1x2 or 2x1) rectangle
        legal_move, remove = [], []

        if not([self.x-1, self.y] in teammate_loc or [self.x-1, self.y] in opponent_loc):
            # left
            legal_move.append([self.x - 2, self.y + 1])
            legal_move.append([self.x - 2, self.y - 1])
        if not([self.x, self.y+1] in teammate_loc or [self.x, self.y+1] in opponent_loc):
            # down
            legal_move.append([self.x - 1, self.y + 2])
            legal_move.append([self.x + 1, self.y + 2])
        if not([self.x+1, self.y] in teammate_loc or [self.x+1, self.y] in opponent_loc):
            # right
            legal_move.append([self.x + 2, self.y + 1])
            legal_move.append([self.x + 2, self.y - 1])
        if not ([self.x, self.y-1] in teammate_loc or [self.x, self.y-1] in opponent_loc):
            # up
            legal_move.append([self.x - 1, self.y - 2])
            legal_move.append([self.x + 1, self.y - 2])

        for move in legal_move:
            # check if x position out of game board
            if move[0] > 8 or move[0] < 0 or move[1] > 9 or move[1] < 0 \
                    or move in teammate_loc:
                remove.append(move)

        for el in remove:
            legal_move.remove(el)

        return legal_move

    def update_coordinate(self, x, y):
        self.x = x
        self.y = y
        self.rect[0] = board_position[self.y][self.x][0]
        self.rect[1] = board_position[self.y][self.x][1]
