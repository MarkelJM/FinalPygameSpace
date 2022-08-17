class Game(Scenes):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        bg_file = os.path.join("resources", "images", "background2.png")
        self.background = pg.image.load(bg_file)
        self.x_margin = 20
        self.player = Plane(midleft=(self.x_margin, HEIGHT/2))

        self.rocks_groups_small = self.rock_group_small()  # create method attribute
        #self.rocks_groups_medium = self.rock_group_medium()
        self.rocks_groups_large = self.rock_group_large()  # create method attribute
        self.activate_level_control = False
        self.lifes_counter = LifesCounting(
            LIFES, self.activate_level_control)  # create class attribute
        #self.levels = Levels(self.player)
        # se crean los planetas, pero están escondidos a la derecha del plano
        self.level1_planet = Level_1(self.player)  # create class attribute
        self.level2_planet = Level_2(self.player)  # create class attribute
        self.level3_planet = Level_3(self.player)  # create class attribute
        # self.no_life = LifesCounting.no_lifes()
        self.bullets_groups = self.bullet_group()  # create method attribute
        self.game_end = Game_Over(self.screen)  # create class attribute

        self.pointer = Points()  # create class attribute

        self.clock = pg.time.Clock()  # time attribute, but not the timing
        self.level_window = Window(self.screen)  # create class attribute
        self.game_finished = Game_ended(self.screen)#game finished pop up, with congrats and to go to HoF

        bullet_effect = os.path.join("resources", "sounds", "shot.wav")
        self.bullet_sound = pg.mixer.Sound(bullet_effect)
        hit_effect = os.path.join("resources", "sounds", "Game_hit.wav")
        self.explosion_sound = pg.mixer.Sound(hit_effect)
        background_music = os.path.join("resources", "sounds", "music.mp3")
        self.music = pg.mixer.music.load(background_music)
        pg.mixer.music.play(-1)

        self.remove_life = 3  # three lifes

    def play(self):
        self.exit = False  # loop breaker variable
        contador_small = 0  # instead of using timing, counting to know when to create small rocks
        # contador_medium = 0   #instead of using timing, counting to know when to create medium rocks
        contador_large = 0  # instead of using timing, counting to know when to create large rocks
        #counting_bullet_time = 0
        self.bullet_timer0 = 0  # instead of using timing, counting to know when to create bullets
        self.shot_exist = False  # boolean to know if shot is created
        self.shot_exist_2 = True  # boolean to know if shot is created 2
        # boolean to activate the option of creating exactly rocks
        self.create_leve_rock = True
        # boolean to determinate if controls are locked
        self.activate_level_control = False
        self.time_start = pg.time.get_ticks()  # game start time
        # variable to know how timing the game is controlled by game
        self.pause_time_controller = 0
        # variable, this number is to don´t disturb level timing later are redefined
        self.pausa_time = 60000
        # variable, this number is to don´t disturb level timing later are redefined
        self.pausa_time2 = 60000
        # variable, this number is to don´t disturb level timing later are redefined
        self.limit_time = 60000
        # variable to know how time gap between real time and level bottom cliced(it shouldn´t exist)
        self.gap_time = 0
        self.level1 = True  # boolean to activate some level aspects
        self.level2 = False  # boolean to activate some level aspects
        self.level3 = False  # boolean to activate some level aspects
        self.level1_active = False  # boolean to activate some level aspects
        self.level2_active = False  # boolean to activate some level aspects
        self.level3_active = False  # boolean to activate some level aspects
        self.a = 0  # variable, because planet and plane hit is continusly hits, so it controls how many times gives points
        self.b = 0  # variable, because planet and plane hit is continusly hits, so it controls how many times gives points
        # as plane is hidden behing planet to stop collision pointer counting(just once)
        self.c = 0  # variable, because planet and plane hit is continusly hits, so it controls how many times gives points
        self.game_over_active = False # to activate event in game over pop up and go back to Home
        self.game_ended = False #pop up antes del hall of fame, mensaje de juego terminado 
        while not self.exit:

            self.time_loop = pg.time.get_ticks()  # each loop timing
            self.timer = self.get_level_time_controller(
                self.time_start, self.time_loop)
            # control all level aspects, levels, windows etc.
            """self.timer está en desarrollo"""
            contador_small += 1  # increase each loop allows to controll when  creat rock
            #contador_medium +=1
            contador_large += 1

            for event in pg.event.get():
                if self.game_over_active == True and event.type == pg.KEYDOWN and event.key == pg.K_x:
                    self.exit = True
                if self.game_ended == True and event.type == pg.KEYDOWN and event.key == pg.K_w:
                    self.exit = True

                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:

                    # if counting_bullet_time == 0 or counting_bullet_time % 10 == 0:
                    bullet_time = self.time_loop - self.bullet_timer0
                    if self.bullet_timer0 == 0 or bullet_time >= 1000:
                        """if shot control are active  it is possible to shot every X seconds"""
                        if self.activate_level_control == False and self.shot_exist_2 == True:

                            self.shot = self.create_bullet()
                            self.shot = self.create_bullet()
                            self.shot = self.create_bullet()
                            self.bullet_sound.play()
                            self.shot_exist == True

                    #counting_bullet_time += 1
                        # to control as before mentioned when to be able to shot
                        self.bullet_timer0 = pg.time.get_ticks()

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            ### ROCK CREATER CONTROLLER ###
            # create first rocks to don´t have problems with create method
            if self.create_leve_rock == True and contador_small == 1 or contador_small % 20 == 0:
                self.created_rock_small = self.create_rocks_small()
            # if self.create_leve_rock == True and contador_medium == 1 or contador_medium % 5 == 0:
                #self.created_rock_medium = self.create_rocks_medium()
            if self.create_leve_rock == True and contador_large == 1 or contador_large % 20 == 0:
                self.created_rock_large = self.create_rocks_large()

            ### UPDATE OBJECTS SETUP ###

            self.player.update(self.activate_level_control)

            if self.shot_exist:

                self.bullet_object.update()
            self.bullets.update()

            self.rock_object_small.update()
            self.rocks_small.update()

            # self.rock_object_medium.update()
            # self.rocks_medium.update()

            self.rock_object_large.update()
            self.rocks_large.update()
            ###  UPDATE PLANET MOVEMENT IF  EACH LEVEL BOOLEAN IS ACTIVATED  ###
            if self.level1_active:
                self.level1_planet.update_planet1(
                    self.activate_level_control, self.player)
                self.planet_group.update()
            if self.level2_active:
                self.level2_planet.update_planet2(
                    self.activate_level_control, self.player)
                self.planet_group.update()
            if self.level3_active:
                self.level3_planet.update_planet3(
                    self.activate_level_control, self.player)
                self.planet_group.update()
            ### KNOW IF COLLISION ARE EXISTING  ###
            plane_crash_small = pg.sprite.spritecollide(
                self.player, self.rocks_small, True)  # plane-rock crask
            rock_small_bullet_crash = pg.sprite.groupcollide(
                self.rocks_small, self.bullets, False, True, pg.sprite.collide_mask)  # plane-rock crask
            """
            plane_crash_medium = pg.sprite.spritecollide(
                self.player, self.rocks_medium, True)  # plane-rock crask
            rock_medium_bullet_crash = pg.sprite.groupcollide(
                self.rocks_medium, self.bullets, False, True, pg.sprite.collide_mask)
            """
            plane_crash_large = pg.sprite.spritecollide(
                self.player, self.rocks_large, True)  # plane-rock crask
            rock_large_bullet_crash = pg.sprite.groupcollide(
                self.rocks_large, self.bullets, False, True, pg.sprite.collide_mask)
            ### POINTER ###

            if rock_small_bullet_crash:
                for rock in rock_small_bullet_crash:
                    for bullet in rock_small_bullet_crash[rock]:
                        rock_life = self.rock_object_small.rock_lost_life()  # IF CRASK ROCK LOST LIFE
                        self.explosion_sound.play()  # explosion sound done
                        if rock_life == 0:  # if lifes 0 gives point and remove the rock
                            self.pointer.increase_points(15)
                            self.rocks_small.remove(rock)
            """ 
            if rock_medium_bullet_crash:
                for rock in rock_medium_bullet_crash:
                    for bullet in rock_medium_bullet_crash[rock]:
                        rock_life = self.rock_object_medium.rock_lost_life()
                        self.explosion_sound.play()
                        if rock_life == 0:
                            self.pointer.increase_points(10)
                            self.rocks_medium.remove(rock)
            """
            if rock_large_bullet_crash:  # as before mentioned with small rocks
                for rock in rock_large_bullet_crash:
                    for bullet in rock_large_bullet_crash[rock]:
                        rock_life = self.rock_object_large.rock_lost_life()
                        self.explosion_sound.play()
                        if rock_life == 0:
                            self.pointer.increase_points(5)
                            self.rocks_large.remove(rock)

            """implementar para que salga de game cuando vidas  se queden en 0"""
            ### PLANE CRASH CONTROLLER ###
            if plane_crash_small and self.activate_level_control == False:
                # plane lost a life if crashed small rock
                self.remove_life = self.lifes_counter.lost_life()
            """    
            if plane_crash_medium and self.activate_level_control == False:
                self.remove_life = self.lifes_counter.lost_life()
            """
            if plane_crash_large and self.activate_level_control == False:  # as small rock
                self.remove_life = self.lifes_counter.lost_life()

            # self.screen.fill(BACKGROUND_COLOUR)
            ###  PAINT BACKGROUND METHOD    ###
            self.paint_background()

            self.planet_group.draw(self.screen)
            ### POP UP A WINDOW TO SHOW A MESSAGE IF YOU PASSED/WIN THE  LEVEL  ###
            if self.plane_in_planet1:  # level window
                self.screen.blit(self.level_window.image,
                                 self.level_window.rect)
                self.message_completed = "NIVEL COMPLETADO"
                self.level_window.draw_text(self.message_completed)
                self.level_window.draw_points(self.pointer.value)
                self.level_window.click_continue()  # pop up of bottom

            self.screen.blit(self.player.image, self.player.rect)  # PLayer

            # draw in the game rocks

            self.rocks_small.draw(self.screen)
            # self.rocks_medium.draw(self.screen)
            self.rocks_large.draw(self.screen)
            # draw bullet

            self.bullets.draw(self.screen)

            # draw points counting
            self.pointer.draw_points(self.screen)

            # draw lifes counting
            self.lifes_counter.paint_lifes(self.screen)

            # level and planet draw

            if self.activate_level_control:
                self.planet_group.draw(self.screen)
                self.planet_group.update()
            ### GAME OVER POP UP ###
            if self.remove_life <= 0:
                print("no vidas")
                self.screen.blit(self.game_end.image, self.game_end.rect)
                self.game_over_message = "GAME OVER"
                self.game_end.draw_text(self.game_over_message, 300)
                self.restart = "Pulsa 'X' para ir a Inicio"
                self.game_end.draw_text(self.restart, HEIGHT - 100)
                self.game_over_active = True
                pg.mixer.music.pause()

            if self.game_ended == True:
                print("juego terminado")
                self.screen.blit(self.game_finished.image, self.game_finished.rect)
                self.congratulation_text = "¡FELICIDADES, JUEGO TERMINADO!"
                self.game_end.draw_text(self.congratulation_text, 300)
                self.HoF_message = "Pulsa 'W' para ir a Inicio"
                self.game_end.draw_text(self.HoF_message, HEIGHT - 100)
                self.game_over_active = True
                pg.mixer.music.pause()

            pg.display.flip()
            self.clock.tick(FPS)

    # background method
    def paint_background(self):
        self.screen.blit(self.background, (0, 0))

    def bullet_group(self):
        self.bullets = pg.sprite.Group()
        self.bullets.empty()

    def create_bullet(self):
        pos_x = (self.player.rect.x) + 50
        pos_y = self.player.rect.y + 15

        self.bullet_object = Bullet(pos_x, pos_y)
        self.bullets.add(self.bullet_object)

    ### Create Rock group ###

    def rock_group_small(self):

        self.rocks_small = pg.sprite.Group()
        self.rocks_small.empty()

    def create_rocks_small(self):
        if self.create_leve_rock == True:
            pos_x = WIDTH
            repeated = randint(0, MAXIMUM_REPEATED_ROCKS_LEVEL)
            for i in range(repeated):
                pos_y = randint(0, HEIGHT)
                self.rock_object_small = Rock_small(pos_x, pos_y)
                self.rocks_small.add(self.rock_object_small)

        """
        if self.create_leve_rock == True:
            pos_x = WIDTH
            pos_y = randint(0, HEIGHT)
            self.rock_object_small = Rock_small(pos_x, pos_y)
            self.rocks_small.add(self.rock_object_small)
            """

    def remove_rock_small(self, rock):
        self.rocks_small.remove(rock)

    """
    def rock_group_medium(self):

        self.rocks_medium = pg.sprite.Group()
        self.rocks_medium.empty()

    def create_rocks_medium(self):
        if self.create_leve_rock == True:
            pos_x = WIDTH
            repeated = randint(0, MAXIMUM_REPEATED_ROCKS_LEVEL)
            for i in range(repeated):
                pos_y = randint(0, HEIGHT)
                self.rock_object_medium = Rock_medium(pos_x,pos_y)
                self.rocks_medium.add(self.rock_object_medium)
    def remove_rock_medium(self, rock):
        self.rocks_medium.remove(rock)
    """

    def rock_group_large(self):

        self.rocks_large = pg.sprite.Group()
        self.rocks_large.empty()

    def create_rocks_large(self):
        if self.create_leve_rock == True:
            pos_x = WIDTH
            repeated = randint(0, MAXIMUM_REPEATED_ROCKS_LEVEL)
            for i in range(repeated):
                pos_y = randint(0, HEIGHT)
                self.rock_object_large = Rock_large(pos_x, pos_y)
                self.rocks_large.add(self.rock_object_large)

    def remove_rock_large(self, rock):
        self.rocks_large.remove(rock)

    def get_level_time_controller(self, time0, time1):
        # to know each loop time, to know in which level should be
        self.real_time = (time1 - time0)

        self.planet_group = pg.sprite.GroupSingle()
        self.plane_in_planet1 = False
        self.plane_in_planet2 = False
        self.plane_in_planet3 = False
        # print(self.real_time)
        if self.real_time < 30000:  # level 1 timing and booleans
            #self.level1 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True

            print("level 1")

        elif 30000 + self.gap_time + self.pausa_time <= self.real_time < self.limit_time + 60000:
            # level 2 timing and booleans
            self.level2 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True

            print("level2")

        elif self.limit_time + 5000 + self.pausa_time2 + self.gap_time <= self.real_time < self.limit_time + 120000:
            # level 3 timing and booleans
            self.level3 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True

            print("level 3")
        else:
            """if it is not in level is because thanks to time controler, like gap, limit and pauses
            means that planet are in movement, plane control activated etc and window pop up is shown
            """
           # print("niveles")
            self.create_leve_rock = False

            # pause_time_controller = pg.time.get_ticks()
            if self.rock_object_small.rect.x <= - 20:  # when last rock created is out screen the controll starts

                self.activate_level_control = True
                self.shot_exist_2 = False
                if self.level1:
                    self.planet_group.add(self.level1_planet)
                    self.level1_active = True
                if self.level2:
                    self.planet_group.remove(self.level1_planet)
                    self.planet_group.add(self.level2_planet)
                    self.level2_active = True
                if self.level3:
                    self.planet_group.remove(self.level2_planet)
                    self.planet_group.add(self.level3_planet)
                    self.level3_active = True
                if self.level1_active:
                    #self.levels.update_planet1(self.activate_level_control, self.player)
                    """
                    rect de planeta da error comprobar
                    """

                    self.plane_in_planet1 = pg.sprite.spritecollide(
                        self.player, self.planet_group, False)

                if self.level2_active:

                    #self.level2_planet.update_planet2(self.activate_level_control, self.player)
                    self.plane_in_planet2 = pg.sprite.spritecollide(
                        self.player, self.planet_group, False)
                if self.level3_active:
                    #self.level3_planet.update_planet3(self.activate_level_control, self.player)
                    self.plane_in_planet3 = pg.sprite.spritecollide(
                        self.player, self.planet_group, False)

                if self.plane_in_planet1:
                    # as plane and planet hit all the time(during this time) just increase once all the level points
                    if self.a == 0:
                        self.pointer.increase_points(100)
                        self.a += 1
                if self.plane_in_planet2:
                    if self.b == 0:  # as before
                        self.b += 1
                        self.pointer.increase_points(200)
                if self.plane_in_planet3:
                    if self.c == 0:  # as before
                        self.c += 1
                        self.pointer.increase_points(400)

                # self.level_window.draw_points(self.pointer.value)

                # self.level_window.click_continue()
                # self.level_window.draw_text()

                for event in pg.event.get():  # as main event checker are locked to dont creeate shots etc
                    # new event checr to exit and to know if mouse is clicking in continue bottom
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pressed_key = pg.mouse.get_pressed()
                        mouse_pos = pg.mouse.get_pos()
                        if pressed_key[0] and 80 <= mouse_pos[0] <= 447 and 165 <= mouse_pos[1] <= 261:
                            # mouse clicking area

                            # indicarlo en el init como pausa_time_controller= 0
                            self.pause_time_controller = pg.time.get_ticks()
                            self.gap_time = self.pause_time_controller - self.real_time
                            if self.level1 == True:  # adapt timer for nexts levels, before game restart
                                self.pausa_time = (
                                    self.pause_time_controller - 30000)

                                self.limit_time = 30000 + self.pausa_time - 2000
                                self.level1 = False
                                #self.rect = self.image.get_rect(midleft=(self.x_margin, HEIGHT/2))

                                print("aqui 1")
                                # print(self.pause_time_controller)
                                # print(self.real_time)
                                # print(self.gap_time)
                                # print(self.pausa_time)
                                # print(self.limit_time)

                            elif self.level2 == True:  # adapt timer for next level, before game restart
                                print("aqui 2")
                                self.pausa_time2 = (
                                    self.pause_time_controller - self.limit_time + 60000)
                                self.limit_time = 30000 + self.pausa_time
                                self.level2 = False

                                self.player.rect.midleft
                                # print(self.real_time)
                                # print(self.gap_time)
                                # print(self.pause_time_controller)
                                # print(self.pausa_time2)
                                # print(self.limit_time)
                            elif self.level3 == True:  # adapt timer for the last level, before game restart
                                print("aqui 3")
                                self.pausa_time2 = (
                                    self.pause_time_controller - self.limit_time + 60000)
                                self.limit_time = 60000 + 30000
                                self.level3 = False
                                self.player.rect.midleft
                               # print(self.pausa_time2)
                                # print(self.limit_time)
                            if self.level1 == False and self.level2 == False and self.level3 == False:
                                # to know that game has ended and Hall Of Fame scene should start

                                print("termino")

    def change_Home_Information(self):
        return False

    def change_Home_Game(self):
        return False

    def change_Information_Home(self):
        return False

    def change_Information_Game(self):
        return False

    def change_Game_Home(self): #read message!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """!!!!!!!!!!currently not working to decide if it should work or not"""
        key = pg.key.get_pressed()
        if key[pg.K_e]:
            return True
    def change_HallofFame_Home(self):
        return False

    def game_over(self):
        key = pg.key.get_pressed()
        if key[pg.K_x]:
            return True
    
    def game_finished(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            return True