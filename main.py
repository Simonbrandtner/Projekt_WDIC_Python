"""main page"""
from random import randint, uniform
from time import time

from enemy import Enemy
from high_scores_screen import screen_scores
from register import (BESTSCORE, NAMEID, PLAYING, SCORE, height, pickle,
                      scores, screen, width)
from variables import (BESTSCOREBEATEN, BESTSCOREPATH, DAMAGE, DAMAGEPATH,
                       
                       DUCKSTATE, HEALING, HEALINGPATH, JUMPING, JUMPPATH,
                       LOST, LOSTPATH, SCORE1000PATH, SCOREPATH,
                       SONICSTANDINGSTATE, SONICSTATE, TIMEJUMP,
                       best_score_rect, best_score_surface, best_score_time,
                       cloud_2_rect, cloud_rect, effect_time, end_font,
                       end_rect, end_surface, end_time, enemies,
                       enemy_bird_surface, enemy_spike_surface, game_over_rect,
                       game_over_surface, grass_2_rect, grass_3_rect,
                       grass_rect, grass_surface, heart_rect, heart_surface,
                       last_score_rect, last_score_surface, palm_2_rect,
                       palm_rect, pseudo_rect, pseudo_surface, restart_rect,
                       restart_surface, rock_surface, score_font,
                       score_live_font, scores_screen_rect,
                       scores_screen_surface, sonic_1_rect, sonic_jump_rect,
                       sonic_jump_surface, sonic_rect, start_jump, states_duck,
                       states_sonic, time_gif, time_gif_duck, time_score_sound,
                       time_spawn, timer, enemy_skydrifter_surface,coin_surface)

try:
    import pygame
except ModuleNotFoundError:
    print("""Vous n'avez pas téléchargé le module pygame ! \n
        Téléchargez le avec la commande ci-contre : pip install pygame""")
from functions import animate_gif, play_sound

coin_speed = 2  # Beispielgeschwindigkeit, passen Sie sie an die Geschwindigkeit der Gegner an
class Coin:
    def __init__(self, surface, spawn_area, speed):
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.spawn_area = spawn_area
        self.speed = speed
        self.spawn()

    def spawn(self):
        """Spawnt den Coin in einem definierten Bereich."""
        x = width  # Setzen von x auf die Breite des Bildschirms
        y = randint(self.spawn_area[2], self.spawn_area[3])
        self.rect.topleft = (x, y)

    def move_like_enemy(self):
        """Bewegt den Coin ähnlich wie einen Gegner."""
        self.rect.x -= self.speed

    def display(self, screen):
        """Zeichnet den Coin."""
        screen.blit(self.surface, self.rect)
    
    def enemy_restriction(self):
        """Überprüft, ob die Münze außerhalb des Spielbereichs ist."""
        return self.rect.x < 0  #  eine  Bedingung, die den linken Rand definiert

coin = Coin(coin_surface, spawn_area=(0, width, 0, height), speed=5)  
coin_spawn_timer = time()
active_coins = []

coin_counter = 0  # Variable für den Münzenzähler

while PLAYING:

    coin_count_surface = score_font.render(f"Coins: {coin_counter}", True, (0, 0, 0))
    coin_count_rect = coin_count_surface.get_rect(bottomright=(width - 10, height - 10))
    screen.blit(coin_count_surface, coin_count_rect)
    
    for coin in active_coins:
        coin.move_like_enemy()
        coin.display(screen)
        if sonic_jump_rect.rect.colliderect(coin.rect):  # Überprüfen , ob Sonic eine Münze gesammelt hat
            coin_counter += 1  # Erhöhen  des Münzenzähler
            active_coins.remove(coin)  # Entfernen  der gesammelten Münze

    active_projectiles = []  # Liste für aktive Projektile
    ACCELERATION = SCORE / 2
    ACCELERATION = min(ACCELERATION, 666)
    #####################
    #ACTIONS DES TOUCHES#
    #####################
    for event in pygame.event.get():
        state_game = LOST and time() - end_time > 3
        if event.type == 256:
            PLAYING = False
        elif event.type == 1024:
            width_restrict = end_rect.left < event.pos[0] < end_rect.right
            height_restrict = end_rect.top < event.pos[1] < end_rect.bottom
            score_w_restrict = scores_screen_rect.left < event.pos[0] < scores_screen_rect.right
            score_h_restrict = scores_screen_rect.top < event.pos[1] < scores_screen_rect.bottom
            if width_restrict and height_restrict and state_game:
                end_surface = end_font.render("CLOSE", True, (255, 60, 60))
            else:
                end_surface = end_font.render("CLOSE", True, (0, 0, 0))
            if score_w_restrict and score_h_restrict and state_game:
                scores_screen_surface = end_font.render(
                    "HIGHSCORES", True, (255, 60, 60))
            else:
                scores_screen_surface = end_font.render(
                    "HIGHSCORES", True, (0, 0, 0))
        elif event.type == 1025 and event.button == 1:
            # on presse le bouton close
            if width_restrict and height_restrict and state_game:
                PLAYING = False
            # on presse le bouton highscores
            if score_w_restrict and score_h_restrict and state_game:
                PLAYING = screen_scores(True)
        elif event.type == 768:
            if event.key == 32 and time() - end_time > 3:
                # on peut sauter
                if sonic_jump_rect.on_floor():
                    start_jump = time()
                    JUMPING = True
                    sonic_jump_rect.change_speed(
                        (0, 1300 - ACCELERATION / 2.5))
                    if time() - best_score_time > 0.5:
                        play_sound(JUMPPATH, 0.02)
                if LOST:
                    LOST = False
                    score_timer = time()
                    SCORE = 0
        elif event.type == 769:
            if event.key == 32:
                if ACCELERATION > 500:
                    FALLINGSPEED = 500
                else:
                    FALLINGSPEED = ACCELERATION
                sonic_jump_rect.change_speed((0, -500 - FALLINGSPEED / 1.3))
    ################
    #SPAWN DES MOBS#
    ################
    # on fait spawn les mobs, avec un délais qui empêche les situations impossibles
    mobs_speed = 850 + ACCELERATION
    delay_mobs = 150 * 4.8 / mobs_speed
    if time() >= time_spawn + delay_mobs + uniform(-0.05, 0.7) and not LOST:
        EASTEREGG = -1
        try:
            CHECKHEART = enemies[len(enemies)-1].category != "heart"
            CHECKHEART2 = enemies[len(enemies)-2].category != "heart"
        except IndexError:
            CHECKHEART = False
        if sonic_1_rect.health == 1:
            random_heart = randint(1, 25)
            EASTEREGG = randint(1, 1000)
        elif sonic_1_rect.health == 2:
            random_heart = randint(1, 55)
        elif sonic_1_rect.health == 3:
            random_heart = randint(1, 100)
        elif sonic_1_rect.health == 4:
            random_heart = randint(1, 100)
        if sonic_1_rect.health == 5:
            random_heart = randint(1, 200)

        mob_type_chance = randint(1, 2)  # 1 für fliegenden Mob, 2 für Boden Mob

        if mob_type_chance == 1:
            # Nur fliegende Mobs
            flying_enemy_chance = randint(1, 2)  # Zufallsauswahl für fliegenden Mob
            if flying_enemy_chance == 1:
                # SkyDrifter
                enemies.append(Enemy(
                    enemy_skydrifter_surface.get_rect(topleft=(width, randint(100, height - 200))),
                    enemy_skydrifter_surface, "flyingMob2")
                )
            else:
                # Bird
                enemies.append(Enemy(
                    enemy_bird_surface.get_rect(topleft=(width, 300)),
                    enemy_bird_surface, "flyingMob")
                )

        else:
            # Nur Boden Mobs
            ground_enemy_chance = randint(1, 3)  # Zufallsauswahl für Boden Mob
            if ground_enemy_chance == 1:
                # Stein
                enemies.append(Enemy(
                    rock_surface.get_rect(topleft=(width, height - 200)),
                    rock_surface, "littleMob")
                )
            elif ground_enemy_chance == 2:
                # Spike
                enemies.append(Enemy(
                    enemy_spike_surface.get_rect(topleft=(width, height - 200)),
                    enemy_spike_surface, "bigMob")
                )
            else:
                # Duck
                enemies.append(Enemy(
                    states_duck[DUCKSTATE].get_rect(topleft=(width, height - 200)),
                    states_duck[DUCKSTATE], "mediumMob")
                )

        if EASTEREGG == 1:
            for i in range(4):
                enemies.append(Enemy(heart_surface.get_rect(topleft=(
                    width,
                    height - randint(200, 700)
                )),
                    heart_surface, "heart")
                )
        time_spawn = time()


        current_time = pygame.time.get_ticks() / 1000  # Aktuelle Zeit in Sekunden
    for enemy in enemies:
        if current_time - enemy.last_shot_time >= 2:  # Alle 2 Sekunden schießen
            projectile = enemy.shoot((255, 0, 0), 5, (5, 0), (0, 0))  # Farbe, Radius, Geschwindigkeit, Offset
            active_projectiles.append(projectile)
            enemy.last_shot_time = current_time

    coin_count_surface = score_font.render(f"Coins: {coin_counter}", True, (0, 0, 0))
    coin_count_rect = coin_count_surface.get_rect(bottomright=(width, height))
    screen.blit(coin_count_surface, coin_count_rect)



    # tick de la frame
    tick = timer.tick(200) / 1000
    ###################################
    #LES FONDS --> LES DEGATS ET HEALS#
    ###################################
    # on affiche l'effet visuel de dégats(fond rouge)
    # pendant 0.25s, et de HEALING (fond vert) (default : blanc)
    effect_delay = time() - effect_time
    if DAMAGE and effect_delay < 0.25:
        screen.fill((255, 100, 100))
    elif HEALING and effect_delay < 0.25:
        screen.fill((100, 255, 100))
    else:
        screen.fill((135, 206, 235))
        effect_time = time()
        DAMAGE = False
        HEALING = False
    
   # Überprüfung, ob 3 Sekunden seit dem letzten Münzen-Spawn vergangen sind
    if time() - coin_spawn_timer > 3:
        # Erzeugen einer neuen Münze und Hinzufügen zur Liste der aktiven Münzen
        new_coin = Coin(coin_surface, spawn_area=(0, width, 0, height), speed=5)
        active_coins.append(new_coin)
        # Aktualisieren des Münzen-Spawn-Timers
        coin_spawn_timer = time()

    # Bewegen und Anzeigen aller aktiven Münzen
    for coin in active_coins:
        coin.move_like_enemy()
        coin.display(screen)

    # Entfernen von Münzen, die außerhalb des Spielbereichs sind
    active_coins = [c for c in active_coins if not c.enemy_restriction()]

    ############
    #LES SCORES#
    ############
    # si on a pas perdu on affiche le score actuel, sinon le last score
    if not LOST:

        SCORE = int(round((time() - score_timer) * 10, 0))
        if BESTSCOREBEATEN:
            score_surface = score_live_font.render(
                f"{SCORE}", True, (255, 195, 36))
        else:
            score_surface = score_live_font.render(f"{SCORE}", True, (0, 0, 0))
    if BESTSCORE < SCORE:
        BESTSCORE = SCORE
        if not BESTSCOREBEATEN:
            play_sound(BESTSCOREPATH, 0.05)
            best_score_time = time()
        BESTSCOREBEATEN = True
    ############
    #ON A PERDU#
    ############
    

    
        
    if sonic_1_rect.health == 0:
        for i in range(len(enemies)):
            enemies.pop(0)
        LOST = True
        BESTSCOREBEATEN = False
        LASTSCORE = SCORE
        last_score_surface = score_font.render(
            f"Last score : {LASTSCORE}", True, (0, 0, 0))
        best_score_surface = score_font.render(
            f"Best score : {BESTSCORE}", True, (0, 0, 0))
        sonic_1_rect.health = 5
        play_sound(LOSTPATH, 0.06)
        end_time = time()
        scores[NAMEID] = BESTSCORE
        with open("best_score.pickle", "wb") as f:
            pickle.dump(scores, f)
    

    ############
    #LES DECORS#
    ############
    if not LOST:
        grass_rect.animate(mobs_speed, 0, tick, screen)
        grass_2_rect.animate(mobs_speed, 0, tick, screen)
        grass_3_rect.animate(mobs_speed, 0, tick, screen)
        cloud_rect.animate(620, 0, tick, screen)
        cloud_2_rect.animate(550, 0, tick, screen)
        palm_rect.animate(475, 0, tick, screen)
        palm_2_rect.animate(475, 0, tick, screen)
    else:
        cloud_rect.animate(160, 0, tick, screen)
        cloud_2_rect.animate(70, 0, tick, screen)
        palm_rect.position = (width / 4, height - 200)
        palm_2_rect.position = (width / 1.3, height - 200)
        palm_rect.animate(0, 0, tick, screen)
        palm_2_rect.animate(0, 0, tick, screen)

    ##############
    #LES ENNEMIES#
    ##############
    enemies_to_pop = []
    for enemy in enemies:
        if not enemy.moving():
            enemy.run(mobs_speed)
        enemy.change_position(tick)
        # si un coeur touche sonic
        if enemy.rect.colliderect(sonic_jump_rect.rect) and enemy.category == "heart":
            if time() - best_score_time > 0.5:
                play_sound(HEALINGPATH, 0.1)
            if sonic_1_rect.health < 7:
                sonic_1_rect.health += 1
            HEALING = True
            enemies_to_pop.append(enemies.index(enemy))
        # si un ennemie touche sonic ...
        elif enemy.rect.colliderect(sonic_jump_rect.rect):
            if time() - best_score_time > 0.5:
                play_sound(DAMAGEPATH, 0.1)
            DAMAGE = True
            sonic_1_rect.health -= 1
            enemies_to_pop.append(enemies.index(enemy))
        # si un ennemie atteind le mur
        elif enemy.enemy_restriction():
            enemies_to_pop.append(enemies.index(enemy))

        ####################
        #AFFICHAGE DES MOBS#
        ####################
        if enemy.category != "mediumMob":
            enemy.display(screen)
        else:
            screen.blit(states_duck[DUCKSTATE], enemy.rect)
            delay_gif = time() - time_gif_duck
            time_gif_duck, DUCKSTATE = animate_gif(
                0.08, 2, time_gif_duck, DUCKSTATE)
    for i in enemies_to_pop:
        enemies.pop(i)

    #################
    #GESTION DU SAUT#
    #################
    # si on est en cours de saut -> on change la position, sinon on redescend
    if time() - start_jump < TIMEJUMP:
        sonic_jump_rect.change_position(tick)
    else:
        sonic_jump_rect.change_speed((0, -1300 - ACCELERATION))
        start_jump = time()
    ############
    #LES TEXTES#
    ############
    if LOST:
        screen.blit(end_surface, end_rect)
        screen.blit(scores_screen_surface, scores_screen_rect)
        screen.blit(last_score_surface, last_score_rect)
        screen.blit(best_score_surface, best_score_rect)
        screen.blit(pseudo_surface, pseudo_rect)
        # playMusic(mainMusic)
    elif not LOST:
        score_rect = score_surface.get_rect(topright=(width, 10))
        screen.blit(score_surface, score_rect)

    if SCORE % 100 == 0 and SCORE != 0 and SCORE % 1000 != 0 and time() - time_score_sound > 0.2:
        play_sound(SCOREPATH, 0.03)
        time_score_sound = time()
    elif SCORE % 1000 == 0 and SCORE != 0 and time() - time_score_sound > 0.2:
        play_sound(SCORE1000PATH, 0.05)
        time_score_sound = time()

    ########
    #LES PV#
    ########
    # affichage du coeur en fonction des pv de sonic
    if not LOST:
        for i in range(sonic_1_rect.health):
            screen.blit(heart_surface, (heart_rect[0] + i*100, heart_rect[1]))

    ####################
    #AFFICHAGE DU PERSO#
    ####################
    # on restreint les positions de sonic
    sonic_jump_rect.sonic_pos_restriction(sonic_rect)
    # si la speed est passé à 0 -> le saut n'est plus actif
    if sonic_jump_rect.speed[1] == 0:
        JUMPING = False

    if sonic_jump_rect.speed[1] < 0:
        sonic_jump_rect.change_speed((0, -50))

    # si on saute on affiche sonicJump
    if JUMPING and not LOST:
        sonic_jump_rect.change_speed((0, -3))
        screen.blit(sonic_jump_surface, sonic_jump_rect.rect)
    # si on a pas perdu on affiche le gif sonic qui court
    elif not LOST:
        # affichage du gif à la main
        screen.blit(states_sonic[0][SONICSTATE], (100, height - 200 - 144))
        speed_gif = 0.2 - ACCELERATION / 2000 if ACCELERATION < 300 else 0.07
        time_gif, SONICSTATE = animate_gif(speed_gif, 4, time_gif, SONICSTATE)
    # sinon on affiche sonic standing
    else:
        if time() - end_time < 3:
            screen.fill((255, 255, 255))
            screen.blit(game_over_surface, game_over_rect)
        else:
            screen.blit(
                states_sonic[1][SONICSTANDINGSTATE],
                (100, height - 200 - 248)
            )
            screen.blit(restart_surface, restart_rect)
            time_gif, SONICSTANDINGSTATE = animate_gif(
                0.3, 2, time_gif, SONICSTANDINGSTATE)
            screen.blit(grass_surface, grass_surface.get_rect(
                topright=(width, height - 200)))
            screen.blit(grass_surface, grass_surface.get_rect(
                topleft=(0, height - 200)))
    pygame.display.flip()
pygame.display.quit()
