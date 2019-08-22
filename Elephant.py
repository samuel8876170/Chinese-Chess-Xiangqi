import pygame
import os
from Setting import board_position


class Elephant:
    # 0 for red side; 1 for black side
    img = [pygame.image.load(os.path.join('imgs', 'elephant.png')),
           pygame.image.load(os.path.join('imgs', 'elephant_g.png'))]

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
        # This piece can only move as a 2x2 square
        legal_move, remove = [], []

        if [self.x + 1,  self.y + 1] not in teammate_loc and \
                [self.x + 1,  self.y + 1] not in opponent_loc:
            legal_move.append([self.x + 2, self.y + 2])
        if [self.x + 1, self.y - 1] not in teammate_loc and \
                [self.x + 1, self.y - 1] not in opponent_loc:
            legal_move.append([self.x + 2, self.y - 2])
        if [self.x - 1, self.y + 1] not in teammate_loc and \
                [self.x - 1, self.y + 1] not in opponent_loc:
            legal_move.append([self.x - 2, self.y + 2])
        if [self.x - 1, self.y - 1] not in teammate_loc and \
                [self.x - 1, self.y - 1] not in opponent_loc:
            legal_move.append([self.x - 2, self.y - 2])

        for move in legal_move:
            # check if x position out of game board
            if move[0] > 8 or move[0] < 0 or move[1] > 9 or move[1] < 0 \
                    or move in teammate_loc:
                remove.append(move)
            else:
                if self.color == 0:     # confirm color
                    if move[1] > 4:     # check if y position out of red region
                        remove.append(move)
                elif self.color == 1:
                    if move[1] < 5:     # check if y position out of black region
                        remove.append(move)
            # it's impossible to remove the 'move' directly. As its length will decrease but index doesn't change.
            # So, the loop will miss the elements which the previous element has been removed.
            # Index will keep going on, but the element we want to check of the "next index" doesn't exist.
            # Instead, the element we want becomes the old index.
        for el in remove:
            legal_move.remove(el)

        return legal_move

    def update_coordinate(self, x, y):
        self.x = x
        self.y = y
        self.rect[0] = board_position[self.y][self.x][0]
        self.rect[1] = board_position[self.y][self.x][1]
