import pygame
import os
from Setting import board_position


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

    def show_legal_move(self, teammate_loc, opponent_loc):
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

        for el in remove:
            legal_move.remove(el)

        return legal_move

    def update_coordinate(self, x, y):
        self.x = x
        self.y = y
        self.rect[0] = board_position[self.y][self.x][0]
        self.rect[1] = board_position[self.y][self.x][1]
