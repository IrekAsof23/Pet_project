import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359), flags=pygame.NOFRAME)
pygame.display.set_caption("First game -- By Irek")
icon = pygame.image.load('/Users/irek/Desktop/mygame/images/game.png').convert()
pygame.display.set_icon(icon)

# Fon
bg = pygame.image.load("images/fon.png").convert()
# Player
walk_left = [
    pygame.image.load("images/left/l0.png").convert_alpha(),
    pygame.image.load("images/left/l1.png").convert_alpha(),
    pygame.image.load("images/left/l3.png").convert_alpha(),
    pygame.image.load("images/left/l4.png").convert_alpha()
]
walk_right = [
    pygame.image.load("images/right/r0.png").convert_alpha(),
    pygame.image.load("images/right/r1.png").convert_alpha(),
    pygame.image.load("images/right/r2.png").convert_alpha(),
    pygame.image.load("images/right/r3.png").convert_alpha(),
]

# Enemy, ghost
enemy = pygame.image.load("images/ghost.png", ).convert_alpha()
enemy_2 = pygame.image.load("images/ghost2.png").convert_alpha()

enemy_list_in_game = []
enemy2_list2_in_game = []

player_anim_count = 0
bg_z = 0
player_speed = 6
player_x = 150
player_y = 250

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound("sounds/1.mp3")
bg_sound.play(-1)

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2600)

enemy2_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy2_timer, 3070)

label = pygame.font.Font("fonts/OgilvieCyr.ttf", 42)
lose_label = label.render("Вы проиграли!", False, (220, 20, 60))
restart_label = label.render("Играть заново", False, (50, 205, 50))
res_label_rect = restart_label.get_rect(topleft=(180, 200))

fire_ball_count = 10
fire_boll = pygame.image.load("images/Magic/fireball.png").convert_alpha()
fire_bolls = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_z, 0))
    screen.blit(bg, (bg_z + 618, 0))

    if gameplay:

        player_sq = walk_left[0].get_rect(topleft=(player_x, player_y))

        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10

                if el.x < -10:
                    enemy_list_in_game.pop(i)

                if player_sq.colliderect(el):
                    gameplay = False

        if enemy2_list2_in_game:
            for (j, el) in enumerate(enemy2_list2_in_game):
                screen.blit(enemy_2, el)
                el.x -= 10

                if el.x < -10:
                    enemy2_list2_in_game.pop(j)

                if player_sq.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()

        # walk player
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        # jump player
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_z -= 2
        if bg_z == -618:
            bg_z = 0

        if fire_boll:
            for i, el in enumerate(fire_bolls):
                screen.blit(fire_boll, (el.x, el.y))
                el.x += 9

                if el.x > 630:
                    fire_bolls.pop(i)

                if enemy_list_in_game:
                    for index, ene in enumerate(enemy_list_in_game):
                        if el.colliderect(ene):
                            enemy_list_in_game.pop(index)
                            fire_bolls.pop(i)
                if enemy2_list2_in_game:
                    for ie, prom in enumerate(enemy2_list2_in_game):
                        if el.colliderect(prom):
                            enemy2_list2_in_game.pop(ie)
                            fire_bolls.pop(i)

    else:
        screen.fill((47, 79, 79))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, res_label_rect)

        mouse = pygame.mouse.get_pos()
        if res_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            enemy_list_in_game.clear()
            enemy2_list2_in_game.clear()
            fire_bolls.clear()
            fire_ball_count = 10

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(620, 250)))
        if event.type == enemy2_timer:
            enemy2_list2_in_game.append(enemy_2.get_rect(topleft=(620, 249)))

            # fireball move when put on "a"
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_a and fire_ball_count > 0:
            fire_bolls.append(fire_boll.get_rect(topleft=(player_x + 30, player_y + 10)))
            fire_ball_count -= 1
    clock.tick(15)
