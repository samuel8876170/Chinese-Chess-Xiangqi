import pygame
import os
from Setting import board_position


class Car:
    # 0 for red side; 1 for black side
    img = [pygame.image.load(os.path.join('imgs', 'car.png')),
           pygame.image.load(os.path.join('imgs', 'car_g.png'))]

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
            for location in teammate_loc:  # consider teammate collision with path
                if location in legal_move:
                    if move[0] <= location[0] < self.x:
                        remove.append(move)
                    elif move[0] >= location[0] > self.x:
                        remove.append(move)
                    if move[1] <= location[1] < self.y:
                        remove.append(move)
                    elif move[1] >= location[1] > self.y:
                        remove.append(move)

            for location in opponent_loc:  # consider opponent collision with path
                if location in legal_move:
                    if move[0] < location[0] < self.x:
                        remove.append(move)
                    elif move[0] > location[0] > self.x:
                        remove.append(move)
                    if move[1] < location[1] < self.y:
                        remove.append(move)
                    elif move[1] > location[1] > self.y:
                        remove.append(move)

        non_repeated = []
        for element in remove:  # delete redundant repeated legal_move
            if element not in non_repeated:
                non_repeated.append(element)

        for el in non_repeated:
            legal_move.remove(el)

        return legal_move

    def update_coordinate(self, x, y):
        self.x = x
        self.y = y
        self.rect[0] = board_position[self.y][self.x][0]
        self.rect[1] = board_position[self.y][self.x][1]
