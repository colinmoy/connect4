import pygame

def main():
    """ Set up the game and run the main game loop """
    pygame.init()             # Prepare the pygame module for use
    surface_sz = 700          # Desired physical surface size, in pixels

    # Create surface of (width, height) and its window.
    main_surface = pygame.display.set_mode((surface_sz, surface_sz))

    # Import images
    game_icon = pygame.image.load('pichulogo.jpg')
    yellow_chip = pygame.image.load('yellowchip.png')
    red_chip = pygame.image.load('redchip.png')

    # Set up the pygame window
    pygame.display.set_caption('Connect 4 by Colin Moy')
    pygame.display.set_icon(game_icon)

    # Set colors and fonts
    background_color = (0, 0, 150)
    label_font = pygame.font.SysFont("comicsansms", 20)
    header_font = pygame.font.SysFont("comicsansms", 40)

    # Get the names of each player
    player1 = input('Player 1 Name:')
    player2 = input('Player 2 Name:')


    my_clock = pygame.time.Clock()

    # Set starting variable values
    turn = 1
    gravity = 0.1
    available_col1 = 6
    available_col2 = 6
    available_col3 = 6
    available_col4 = 6
    available_col5 = 6
    available_col6 = 6
    available_col7 = 6
    board = [['','','','','','',''],
             ['','','','','','',''],
             ['','','','','','',''],
             ['','','','','','',''],
             ['','','','','','',''],
             ['','','','','','','']]
    all_sprites = []
    tie_state = False

    # Create a playing chip object
    class Chip:

        def __init__(self, img, column, target_posn):
            """ Create and initialize a chip for a target position on the board """
            self.image = img
            self.target_posn = target_posn
            self.posn = (100 * column - 89, 60)
            self.y_velocity = 0

        def update(self):
            self.y_velocity += gravity
            (x,y) = self.posn
            new_y_pos = y + self.y_velocity
            (target_x, target_y) = self.target_posn
            dist_to_go = target_y - new_y_pos

            if dist_to_go < 0:
                self.y_velocity = -0.25 * self.y_velocity
                new_y_pos = target_y + dist_to_go

            self.posn = (x, new_y_pos)

        def draw(self, target_surface):
            target_surface.blit(self.image, self.posn)

    def check_for_win():
        # Check horizontals
        for x in range(6):
            for y in range(4):
                if board[x][y] != '' and board[x][y] == board[x][y+1] == board[x][y+2] == board[x][y+3]:
                    return True

        # Check verticals
        for x in range(3):
            for y in range(7):
                if board[x][y] != '' and board[x][y] == board[x+1][y] == board[x+2][y] == board[x+3][y]:
                    return True

        # Check diagonals (top left to bottom right)
        for x in range(3):
            for y in range(4):
                if board[x][y] != '' and board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3]:
                    return True

        # Check diagonals (top right to bottom left)
        for x in range(3):
            for y in range(3,7):
                if board[x][y] != '' and board[x][y] == board[x+1][y-1] == board[x+2][y-2] == board[x+3][y-3]:
                    return True

    win_state = check_for_win()

    while not win_state and not tie_state:                 # Game loop
        ev = pygame.event.get()

        # Find the coordinates of each of the available spots
        available_spot1 = (50, 12 + 100 * available_col1)
        available_spot2 = (150, 12 + 100 * available_col2)
        available_spot3 = (250, 12 + 100 * available_col3)
        available_spot4 = (350, 12 + 100 * available_col4)
        available_spot5 = (450, 12 + 100 * available_col5)
        available_spot6 = (550, 12 + 100 * available_col6)
        available_spot7 = (650, 12 + 100 * available_col7)

        if available_col1 > 0:
            availabl_spot1 = (50, 50 + 100 * available_col1)
        if available_col2 > 0:
            availabl_spot2 = (150, 50 + 100 * available_col2)
        if available_col3 > 0:
            availabl_spot3 = (250, 50 + 100 * available_col3)
        if available_col4 > 0:
            availabl_spot4 = (350, 50 + 100 * available_col4)
        if available_col5 > 0:
            availabl_spot5 = (450, 50 + 100 * available_col5)
        if available_col6 > 0:
            availabl_spot6 = (550, 50 + 100 * available_col6)
        if available_col7 > 0:
            availabl_spot7 = (650, 50 + 100 * available_col7)


        if turn % 2 == 1:                   # Change the header at the top of the game screen
            player_with_turn = player1
            player_color = 'Yellow'
            text_color = (255, 255, 0)
            chip_image = yellow_chip

            mouse_pos = pygame.mouse.get_pos()
            if 0 < mouse_pos[0] < 100:
                hover = 1
                main_surface.fill(background_color)

                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col1 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot1, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 100 < mouse_pos[0] < 200:
                hover = 2
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col2 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot2, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 200 < mouse_pos[0] < 300:
                hover = 3
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col3 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot3, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 300 < mouse_pos[0] < 400:
                hover = 4
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col4 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot4, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 400 < mouse_pos[0] < 500:
                hover = 5
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col5 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot5, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 500 < mouse_pos[0] < 600:
                hover = 6
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col6 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot6, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 600 < mouse_pos[0] < 700:
                hover = 7
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col7 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot7, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            for event in ev:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 0 < mouse_pos[0] < 100 and available_col1 > 0:
                        turn += 1
                        chip = Chip(chip_image, 1, available_spot1)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col1 - 1][hover - 1] = player_color
                        available_col1 -= 1
                    if 100 < mouse_pos[0] < 200 and available_col2 > 0:
                        turn += 1
                        chip = Chip(chip_image, 2, available_spot2)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col2 - 1][hover - 1] = player_color
                        available_col2 -= 1
                    if 200 < mouse_pos[0] < 300 and available_col3 > 0:
                        turn += 1
                        chip = Chip(chip_image, 3, available_spot3)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col3 - 1][hover - 1] = player_color
                        available_col3 -= 1
                    if 300 < mouse_pos[0] < 400 and available_col4 > 0:
                        turn += 1
                        chip = Chip(chip_image, 4, available_spot4)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col4 - 1][hover - 1] = player_color
                        available_col4 -= 1
                    if 400 < mouse_pos[0] < 500 and available_col5 > 0:
                        turn += 1
                        chip = Chip(chip_image, 5, available_spot5)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col5 - 1][hover - 1] = player_color
                        available_col5 -= 1
                    if 500 < mouse_pos[0] < 600 and available_col6 > 0:
                        turn += 1
                        chip = Chip(chip_image, 6, available_spot6)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col6 - 1][hover - 1] = player_color
                        available_col6 -= 1
                    if 600 < mouse_pos[0] < 700 and available_col7 > 0:
                        turn += 1
                        chip = Chip(chip_image, 7, available_spot7)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col7 - 1][hover - 1] = player_color
                        available_col7 -= 1

            for sprite in all_sprites:
                sprite.update()

            main_surface.fill(background_color)

            for col in range(0,800,100):
                main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                for row in range(100,800,100):
                    pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

            header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
            main_surface.blit(header, (5,5))

            for sprite in all_sprites:
                sprite.draw(main_surface)

            win_state = check_for_win()

            if board[0][0] != '' and board[0][1] != '' and board[0][2] != '' and board[0][3] != '' and board[0][4] != '' and board[0][5] != '' and board[0][6] != '':
                tie_state = True

            pygame.display.flip()

        else:
            player_with_turn = player2
            player_color = 'Red'
            text_color = (255, 0, 0)
            chip_image = red_chip

            mouse_pos = pygame.mouse.get_pos()
            if 0 < mouse_pos[0] < 100:
                hover = 1
                main_surface.fill(background_color)

                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col1 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot1, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 100 < mouse_pos[0] < 200:
                hover = 2
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col2 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot2, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 200 < mouse_pos[0] < 300:
                hover = 3
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col3 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot3, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 300 < mouse_pos[0] < 400:
                hover = 4
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col4 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot4, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 400 < mouse_pos[0] < 500:
                hover = 5
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col5 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot5, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 500 < mouse_pos[0] < 600:
                hover = 6
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col6 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot6, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 600 < mouse_pos[0] < 700:
                hover = 7
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                if available_col7 > 0:
                    pygame.draw.circle(main_surface, (50,50,50), availabl_spot7, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 400 < mouse_pos[0] < 500:
                hover = 5
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                pygame.draw.circle(main_surface, (50,50,50), availabl_spot5, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 500 < mouse_pos[0] < 600:
                hover = 6
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                pygame.draw.circle(main_surface, (50,50,50), availabl_spot6, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            if 600 < mouse_pos[0] < 700:
                hover = 7
                main_surface.fill(background_color)
                for sprite in all_sprites:
                    sprite.update()

                for col in range(0,800,100):
                    main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                    for row in range(100,800,100):
                        pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

                header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
                main_surface.blit(header, (5,5))

                for sprite in all_sprites:
                    sprite.draw(main_surface)

                pygame.draw.circle(main_surface, (50,50,50), availabl_spot7, 45, 0)

                my_clock.tick(60)

                pygame.display.flip()

            for event in ev:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 0 < mouse_pos[0] < 100 and available_col1 > 0:
                        turn += 1
                        chip = Chip(chip_image, 1, available_spot1)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col1 - 1][hover - 1] = player_color
                        available_col1 -= 1
                    if 100 < mouse_pos[0] < 200 and available_col2 > 0:
                        turn += 1
                        chip = Chip(chip_image, 2, available_spot2)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col2 - 1][hover - 1] = player_color
                        available_col2 -= 1
                    if 200 < mouse_pos[0] < 300 and available_col3 > 0:
                        turn += 1
                        chip = Chip(chip_image, 3, available_spot3)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col3 - 1][hover - 1] = player_color
                        available_col3 -= 1
                    if 300 < mouse_pos[0] < 400 and available_col4 > 0:
                        turn += 1
                        chip = Chip(chip_image, 4, available_spot4)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col4 - 1][hover - 1] = player_color
                        available_col4 -= 1
                    if 400 < mouse_pos[0] < 500 and available_col5 > 0:
                        turn += 1
                        chip = Chip(chip_image, 5, available_spot5)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col5 - 1][hover - 1] = player_color
                        available_col5 -= 1
                    if 500 < mouse_pos[0] < 600 and available_col6 > 0:
                        turn += 1
                        chip = Chip(chip_image, 6, available_spot6)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col6 - 1][hover - 1] = player_color
                        available_col6 -= 1
                    if 600 < mouse_pos[0] < 700 and available_col7 > 0:
                        turn += 1
                        chip = Chip(chip_image, 7, available_spot7)
                        all_sprites.append(chip)
                        chip.draw(main_surface)
                        board[available_col7 - 1][hover - 1] = player_color
                        available_col7 -= 1

            for sprite in all_sprites:
                sprite.update()

            main_surface.fill(background_color)

            for col in range(0,800,100):
                main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
                for row in range(100,800,100):
                    pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

            header = header_font.render("{0}'s Turn ({1})".format(player_with_turn, player_color), True, text_color)
            main_surface.blit(header, (5,5))

            for sprite in all_sprites:
                sprite.draw(main_surface)

            win_state = check_for_win()

            if board[0][0] != '' and board[0][1] != '' and board[0][2] != '' and board[0][3] != '' and board[0][4] != '' and board[0][5] != '' and board[0][6] != '':
                tie_state = True

            pygame.display.flip()

    while win_state:
        for sprite in all_sprites:
            sprite.update()

        main_surface.fill(background_color)

        for col in range(0,800,100):
            main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
            for row in range(100,800,100):
                pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

        header = header_font.render("{0} ({1}) wins! (ESC to quit)".format(player_with_turn, player_color), True, text_color)
        main_surface.blit(header, (5,5))

        for sprite in all_sprites:
            sprite.draw(main_surface)

        pygame.display.flip()

        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit

    while tie_state:
        for sprite in all_sprites:
            sprite.update()

        main_surface.fill(background_color)

        for col in range(0,800,100):
            main_surface.blit(label_font.render('{0}'.format(col//100 + 1), True, (0,0,0)), (col+45,75))
            for row in range(100,800,100):
                pygame.draw.circle(main_surface, (0,0,0), [col+50, row+50], 45, 0)

        header = header_font.render("Tie! (ESC to quit)", True, (0,200,0))
        main_surface.blit(header, (5,5))

        for sprite in all_sprites:
            sprite.draw(main_surface)

        pygame.display.flip()

        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit

if __name__ == '__main__':
    main()