import pygame
import Setting
from Setting import win_width, win_height, board_position
import os
from Cannon import Cannon
from Car import Car
from Elephant import Elephant
from Guard import Guard
from Horse import Horse
from King import King
from Minion import Minion

# board setting
board_img = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'chess_board.jpg')), (700, 600))


def draw_background(win, sprites, move_list=None, color=0):
    # generate chess board
    win.fill((231, 201, 129))
    win.blit(board_img, (25, 25))

    # generate piece image and its hit_box
    for sprite in sprites[color]:
        win.blit(sprite.img[color], board_position[sprite.y][sprite.x])
        pygame.draw.rect(win, (255, 0, 0), (board_position[sprite.y][sprite.x][0],
                                            board_position[sprite.y][sprite.x][1],
                                            sprite.rect[2], sprite.rect[3]), 1)
    for sprite in sprites[1 - color]:
        win.blit(sprite.img[1 - color], board_position[sprite.y][sprite.x])
#         pygame.draw.rect(win, (255, 0, 0), (board_position[sprite.y][sprite.x][0],
#                                             board_position[sprite.y][sprite.x][1],
#                                             sprite.rect[2], sprite.rect[3]), 1)

    # generate rect of move_list
    if move_list:
        # print('move_list is True')
        for move in move_list:
            pygame.draw.rect(win, (0, 255, 0), (board_position[move[1]][move[0]][0],
                                                board_position[move[1]][move[0]][1], 61, 61), 1)

    pygame.display.update()


def main():
    # game setting
    pygame.time.Clock()
    pygame.display.init()

    # win setting
    pygame.display.set_caption("Chinese Chess")
    win = pygame.display.set_mode((win_width, win_height))

    # generate pieces sprite of two side ( 0 for red, 1 for black )
    sprites = [[Car(0, 0, 0), Horse(1, 0, 0), Elephant(2, 0, 0),
                Guard(3, 0, 0), King(4, 0, 0), Guard(5, 0, 0),
                Elephant(6, 0, 0), Horse(7, 0, 0), Car(8, 0, 0),
                Cannon(1, 2, 0), Cannon(7, 2, 0), Minion(0, 3, 0),
                Minion(2, 3, 0), Minion(4, 3, 0), Minion(6, 3, 0),
                Minion(8, 3, 0)],
               [Car(0, 9, 1), Horse(1, 9, 1), Elephant(2, 9, 1),
                Guard(3, 9, 1), King(4, 9, 1), Guard(5, 9, 1),
                Elephant(6, 9, 1), Horse(7, 9, 1), Car(8, 9, 1),
                Cannon(1, 7, 1), Cannon(7, 7, 1), Minion(0, 6, 1),
                Minion(2, 6, 1), Minion(4, 6, 1), Minion(6, 6, 1),
                Minion(8, 6, 1)]]

    kings = [sprites[0][4], sprites[1][4]]

    color, sprite, legal_move = 0, 0, []

    draw_background(win, sprites, legal_move, color)
    print('>> Game Start!\n')

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        mouse_pos = pygame.mouse.get_pos()

        if kings[color] not in sprites[color]:
            if color == 0:
                print('Black Win!!')
            elif color == 1:
                print('Red Win!!')
            run = False

        teammates_loc = []
        for teammate in sprites[color]:
            # Save teammate location to let inner function do specific delete of legal_move.
            teammates_loc.append([teammate.x, teammate.y])
            # if [teammate.x, teammate.y] in legal_move:
            #     legal_move.remove([teammate.x, teammate.y])     # you cannot overlap two pieces

        opponents_loc = []
        for opponent in sprites[1 - color]:
            # Save enemy location to let inner function do specific delete of legal_move.
            opponents_loc.append([opponent.x, opponent.y])

        if pygame.mouse.get_pressed()[0]:
            for sprite in sprites[color]:
                if 0 < mouse_pos[0] - sprite.rect[0] < 61 and 0 < mouse_pos[1] - sprite.rect[1] < 61:
                    print('>> mouse_pos:', mouse_pos, 'sprite.rect: (', sprite.rect[0], ',', sprite.rect[1], ')')
                    print('>> you picked up', sprite, ' at point', [sprite.x, sprite.y], 'color:', color, '\n')

                    if id(sprite) == id(kings[color]):
                        legal_move = sprite.show_legal_move(teammates_loc, opponents_loc, kings)
                    else:
                        legal_move = sprite.show_legal_move(teammates_loc, opponents_loc)

                    choose = True   # now choose a destination for your chosen piece
                    if legal_move:
                        print(">> you can choose a destination or you can press 'Esc' to choose another pieces.")
                        while choose:
                            pygame.event.pump()
                            mouse_pos = pygame.mouse.get_pos()  # keep track on mouse_pos and key_pressed
                            key = pygame.key.get_pressed()

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    run, choose = False, False

                            if pygame.mouse.get_pressed()[0]:
                                for move in legal_move:
                                    if 0 < mouse_pos[0] - board_position[move[1]][move[0]][0] < 61 and \
                                            0 < mouse_pos[1] - board_position[move[1]][move[0]][1] < 61:
                                        # update the coordinate system of sprite
                                        if move in opponents_loc:
                                            print('eat~\n')
                                            for piece in sprites[1 - color]:
                                                if move == [piece.x, piece.y]:
                                                    print('deleted')
                                                    sprites[1 - color].remove(piece)
                                                    print(sprites[1-color])
                                        else:
                                            print('>> move~\n')
                                        sprite.update_coordinate(move[0], move[1])

                                        old_position, sprite, legal_move = [], 0, []    # reset all inner var for moving
                                        choose = False

                                        color = 1 - color

                                        pygame.time.wait(500)

                            if key[pygame.K_ESCAPE]:    # back to choosing pieces process
                                print('>> ESC pressed\n')

                                old_position, sprite, legal_move = [], 0, []    # reset all inner var for moving
                                choose = False

                            draw_background(win, sprites, legal_move, color)
                    else:
                        print(">> There is no legal_move! Pick up another pieces.")

        draw_background(win, sprites, legal_move, color)


if __name__ == '__main__':
    main()

pygame.quit()
