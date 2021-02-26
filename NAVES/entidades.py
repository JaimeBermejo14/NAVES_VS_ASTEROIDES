
import pygame as pg
from NAVES import GAME_DIMENSIONS, FPS
import random
import sys
pg.init()

# fuente
pg.font.init()
def create_font(t, s=72, c=(255, 255, 0), b=False, i=False):
    font = pg.font.SysFont("Alien Encounters", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text

battlest = pg.font.Font("recursos/fuentes/BATTLEST.TTF", 90)

# constantes
VIDAS_DEL_JUEGO = 3
GAME_OVER_FONT = create_font("GAME OVER")
SURF = pg.display.set_mode(GAME_DIMENSIONS)

class Planet:
    def __init__(self):
        self.image = pg.image.load("recursos/imagenes/planet-450x461.png")
        self.x = GAME_DIMENSIONS[0]
        self.y = (GAME_DIMENSIONS[1] - pg.Surface.get_height(self.image)) / 2

    def move(self, x, y):
        self.x += x
        self.y += y

    def getWidth(self):
        return pg.Surface.get_width(self.image)

class Nivel:
    def __init__(self, n, m):
        self.stop_level = False
        self.ending_level = False
        self.finish_level = False
        self.bigAsters = []
        self.aster = []
        self.nivel = n
        self.puntos = 0
        self.update_nivel()
        self.meta_nivel = m
        self.finalizando = False
        self.timeleft = pg.time.get_ticks()

    def nivelSound(self):
        pg.mixer.init()
        pg.mixer.music.load("recursos/audio/nivel_.ogg")
        pg.mixer.music.play(-1) 
        pg.mixer.music.set_volume(0.5)

    def update_nivel(self):
        for i in range(random.randint(2 * self.nivel, 5 * self.nivel)):
            ax3 = Asteroidex3()
            ax3.vx = random.randint(2 * self.nivel, 6 * self.nivel)
            self.aster.append(ax3)

        for i in range(1 * self.nivel):
            ax3 = asteroide()
            self.bigAsters.append(ax3)

    def actualizarBigAsters(self):
        for bigAster in self.bigAsters:
            bigAster.actualizar(self.finalizando)

    def actualizarAsters(self):
        for aster in self.aster:
            aster.actualizar(self.finalizando)

    def tieneAsteroides(self):
        totalAsteroides = []
        for bigAster in self.bigAsters:
            totalAsteroides.append(bigAster.rect.x < - pg.Surface.get_width(bigAster.image))
        for aster in self.aster:
            totalAsteroides.append(aster.x < - pg.Surface.get_width(aster.image))
        return not all(totalAsteroides)

    def restart(self):
        self.bigAsters = []
        self.aster = []
        self.update_nivel()
        self.nivelSound()

    def get_numeroNivel(self):
        return self.nivel

class Explote(pg.sprite.Sprite):
    imagenes_files = ['explote100x100_01.png', 'explote100x100_02.png', 'explote100x100_03.png',
                      'explote100x100_04.png', 'explote100x100_05.png',
                      'explote100x100_06.png', 'explote100x100_07.png', 'explote100x100_08.png',
                      'explote100x100_09.png', 'explote100x100_10.png',
                      'explote100x100_11.png', 'explote100x100_12.png', 'explote100x100_13.png',
                      'explote100x100_14.png', 'explote100x100_15.png',
                      'explote100x100_16.png', 'explote100x100_18.png', 'explote100x100_19.png',
                      'explote100x100_20.png']

    def __init__(self):
        super(Explote, self).__init__()
        self.image_act = 0
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]
        self.rect = pg.Rect(5, 5, 150, 198)
        self.ciclos_tras_refresco = 0
        self.retardo_anim = 5

    def update(self):
        self.ciclos_tras_refresco += 1
        if self.ciclos_tras_refresco % self.retardo_anim == 0:
            self.image_act += 1
            if self.image_act >= len(self.imagenes):
                self.image_act = 0
        self.image = self.imagenes[self.image_act]

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"recursos/imagenes/{img}"))
        return lista_imagenes

    def setPosition(self, x, y):
        self.rect.top = y
        self.rect.left = x

    def explote_sound(self):
        pg.mixer.init()
        pg.mixer.music.load("recursos/audio/sonido-1.ogg")
        pg.mixer.music.play()
        pg.mixer.music.set_volume(0.5)

class nave:
    def __init__(self, x, y, vy):
        self.angle = 0
        self.vc = 5   # velocidad de la nave
        self.x = x
        self.y = y
        self.vy = vy
        self.image = pg.image.load("recursos/imagenes/nave-75x50.png")
        self.rect = pg.Surface.get_rect(self.image)
        self.rect.top = y
        self.rect.left = x
        self.setDimension()
        self.printPos = (0, 0)
        self.printImage = self.image

    def getRect(self):
        return self.rect

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setDimension(self):
        self.height = pg.Surface.get_height(self.image)
        self.width = pg.Surface.get_width(self.image)

    def actualizar(self):
        self.y += self.vy
        self.rect.top += self.vy
        if self.y + 50 >= GAME_DIMENSIONS[1]:
            self.y = GAME_DIMENSIONS[1] - 50
            self.rect.top = GAME_DIMENSIONS[1] - 50
        if self.y <= 0:
            self.y = 0
            self.rect.top = 0
        self.printPos = (self.x, self.y)
        self.printImage = self.image
        if self.angle != 0:
            centro_naveX = self.rect.centerx
            centro_naveY = self.rect.centery
            nave_rotadaS = pg.transform.rotozoom(self.image, self.angle, 1)
            rectanguloRot = nave_rotadaS.get_rect(centerx=centro_naveX, centery=centro_naveY)
            self.printPos = rectanguloRot
            self.printImage = nave_rotadaS

    def naveAterrizando(self):
        if self.y < GAME_DIMENSIONS[1] / 2:
            self.y += self.vc
            self.rect.top += self.vc
        if self.y > GAME_DIMENSIONS[1] / 2:
            self.y -= self.vc
            self.rect.top -= self.vc
        if self.y == GAME_DIMENSIONS[1] / 2 and not self.x == GAME_DIMENSIONS[0] - self.width:
            self.x += self.vc
            self.rect.left += self.vc
        if self.x == GAME_DIMENSIONS[0] - self.width and self.angle < 180:
            self.angle += 1
        pg.mixer.init()
        pg.mixer.music.load("recursos/audio/deedle.ogg")
        pg.mixer.music.play() 
        pg.mixer.music.set_volume(0.5)

    def manejar_eventos(self):
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_UP]:
            self.vy = -10
        elif teclas_pulsadas[pg.K_DOWN]:
            self.vy = 10
        else:
            self.vy = 0

class Asteroidex3():
    w = 50
    h = 50

    def __init__(self):
        self.x = -self.w
        self.y = random.randint(0, 550)
        self.vx = 4
        self.image = pg.image.load("recursos/imagenes/aster1-50x50.png")

        self.rect = pg.Surface.get_rect(self.image)

    def actualizar(self, finalizando):
        self.x -= self.vx
        self.rect.x -= self.vx
        if self.x <= -50 and not finalizando:
            self.x = 850
            self.rect.x = 850
            self.y = random.randint(0, 550)
            self.rect.y = self.y
            self.vx = random.randint(2, 10)

class asteroide():
    imagenes_files = ['asteroides_01.png', 'asteroides_02.png', 'asteroides_03.png', 'asteroides_04.png',
                      'asteroides_05.png',
                      'asteroides_06.png', 'asteroides_07.png', 'asteroides_08.png', 'asteroides_09.png',
                      'asteroides_10.png',
                      'asteroides_11.png', 'asteroides_12.png', 'asteroides_13.png', 'asteroides_14.png',
                      'asteroides_15.png',
                      'asteroides_16.png', 'asteroides_18.png', 'asteroides_19.png', 'asteroides_20.png',
                      'asteroides_21.png',
                      'asteroides_22.png', 'asteroides_23.png', 'asteroides_24.png', 'asteroides_25.png',
                      'asteroides_26.png',
                      'asteroides_27.png', 'asteroides_28.png', 'asteroides_29.png', 'asteroides_30.png',
                      'asteroides_31.png']
    retardo_anim = 5  # cuanto mas alto sea el valor mas lenta es la animacion

    def __init__(self):
        self.x = 928
        self.y = random.randint(2, 15)
        self.vx = 5
        self.vy = 0
        self.image_act = 0 # contador empezando en 0
        self.ciclos_tras_refresco = 0
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]
        self.rect = self.image.get_rect(x=self.x, y=self.y)
  
    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"recursos/imagenes/{img}"))
        return lista_imagenes

    def actualizar_posicion(self, finalizando): # Gestionar posicion del asteroide
        if self.rect.x <= -128 and not finalizando:
            self.rect.x = 928
            self.rect.y = random.randint(0, 472)
        self.rect.x -= self.vx

    def actualizar_imagen(self):# Gestionar imagen activa (disfraz de asteroide)
        self.ciclos_tras_refresco += 1
        if self.ciclos_tras_refresco % self.retardo_anim == 0:
            self.image_act += 1
            if self.image_act >= len(self.imagenes):
                self.image_act = 0
        self.image = self.imagenes[self.image_act]

    def actualizar(self, finalizando):
        self.actualizar_posicion(finalizando)
        self.actualizar_imagen()

class Game:
    def __init__(self):
        self.timeLeft = 0
        self.numeroDeNiveles = 2
        self.puntosAcumulados = 0
        self.planet1 = Planet()
        self.clock = pg.time.Clock()
        self.pantalla = pg.display.set_mode(GAME_DIMENSIONS)
        self.bg = pg.image.load("recursos/imagenes/space.png")
        self.bg2 = pg.image.load("recursos/imagenes/Portada-2.png")
        self.bg3 = pg.image.load("recursos/imagenes/Portada-3.png")
        pg.display.set_caption("NAVES")
        self.crash_nave = False
        self.nivel = Nivel(1, random.randint(10, 20)) 
        self.vidas = VIDAS_DEL_JUEGO
        self.puntos = 0
        self.goalRect = pg.Rect(0, 0, 1, 600) 
        self.nave = nave(10, 275, 0)
        self.explote = Explote()

    # bucle principal
    def bucle_principal(self):
        game_over = False
        contador = 0
        self.nivel.nivelSound()

        while not game_over:
            events = pg.event.get()
            self.clock.tick(FPS)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            if not self.nivel.stop_level:
                self.nave.manejar_eventos()
                self.nave.actualizar()
                self.nivel.actualizarAsters()
                self.nivel.actualizarBigAsters()  
                self.pantalla.blit(self.bg, (0, 0))

                allAsters = []
                for aster in self.nivel.aster:
                    allAsters.append(aster.rect)
                    self.pantalla.blit(aster.image, (aster.x, aster.y))
                for bigAster in self.nivel.bigAsters:
                    allAsters.append(bigAster.rect)
                    self.pantalla.blit(bigAster.image, (bigAster.rect.x, bigAster.rect.y))

                if self.nave.rect.collidelistall(allAsters):
                    self.explote.explote_sound()
                    self.nivel.stop_level = True
                    self.crash_nave = True
                    allAsters = []
                self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
                if self.goalRect.collidelistall(allAsters):
                    self.puntos += 1
                if ((pg.time.get_ticks() - self.nivel.timeleft) / 1000) > self.nivel.meta_nivel :
                    self.nivel.finalizando = True
                if ((pg.time.get_ticks() - self.nivel.timeleft) / 1000) > self.nivel.meta_nivel and not self.nivel.tieneAsteroides():
                    self.nivel.stop_level = True
                    self.nivel.ending_level = True
                    self.nave.vy = 0
            if self.nivel.stop_level:
                if self.crash_nave:
                    contador += 1
                    if contador < len(self.explote.imagenes) * self.explote.retardo_anim:
                        self.pantalla.blit(self.bg, (0, 0))
                        self.pantalla.blit(self.explote.image, (self.nave.x, self.nave.y - self.nave.getHeight() / 2))
                        self.explote.update()
                    if contador > 100:
                        self.vidas -= 1
                        contador = 0
                        timeLeft = pg.time.get_ticks()
                        if self.vidas > 0:
                            while ((pg.time.get_ticks() - timeLeft) / 1000) < 2:
                                self.pantalla.blit(self.bg, (0, 0))
                                textoVidas = create_font("Vuelve A Intentarlo", 32, (255, 255, 255))
                                SURF.blit(textoVidas,((GAME_DIMENSIONS[0] - textoVidas.get_width()) / 2, GAME_DIMENSIONS[1] / 2.25))
                                pg.display.flip()
                        else:
                            while ((pg.time.get_ticks() - timeLeft) / 1000) < 5:
                                self.pantalla.blit(self.bg, (0, 0))
                                textoVidas = create_font("Game Over", 32, (255, 255, 255))
                                SURF.blit(textoVidas,((GAME_DIMENSIONS[0] - textoVidas.get_width()) / 2, GAME_DIMENSIONS[1] / 2.25))
                                pg.display.flip()
                            self.irAlaPortada()
                        self.nivel.restart()
                        self.nivel.stop_level = False
                        self.crash_nave = False
                        self.nivel.finalizando = False
                elif self.nivel.ending_level:
                    self.pantalla.blit(self.bg, (0, 0))

                    while self.planet1.x != (GAME_DIMENSIONS[0] - self.planet1.getWidth() / 2):
                        self.planet1.move(-0.25, 0)
                        self.pantalla.blit(self.bg, (0, 0))
                        self.pantalla.blit(self.planet1.image, (self.planet1.x, self.planet1.y))
                        self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
                        pg.display.flip()
                    self.nave.naveAterrizando()
                    self.nave.actualizar()
                    self.pantalla.blit(self.planet1.image, (self.planet1.x, self.planet1.y))
                    self.pantalla.blit(self.nave.printImage, self.nave.printPos)
                    if self.nave.angle == 180:
                        self.nivel.finish_level = True
                        self.nivel.ending_level = False
                        self.timeLeft = pg.time.get_ticks() 

                elif self.nivel.finish_level:
                    if self.nivel.get_numeroNivel() >= self.numeroDeNiveles:
                        while ((pg.time.get_ticks() - self.timeLeft) / 1000) < 2:
                            self.pantalla.blit(self.bg, (0, 0))
                            textLevelComplete = create_font(" Mision Cumplida! ", 32, (255, 255, 255))
                            SURF.blit(textLevelComplete, ((GAME_DIMENSIONS[0] - textLevelComplete.get_width()) / 2, GAME_DIMENSIONS[1] / 2.25))
                            pg.display.flip()

                        tecla_pulsada = pg.key.get_pressed()
                        if tecla_pulsada[pg.K_RETURN]:
                            self.puntosAcumulados = 0
                            self.puntos = 0
                            self.vidas = VIDAS_DEL_JUEGO
                            self.nivel = Nivel(1,random.randint(10, 20))
                            self.nave = nave(10, 275, 0)
                            self.irAlaPortada()
                            self.nivel.nivelSound()

                        if ((pg.time.get_ticks() - self.timeLeft) / 1000) > 5:
                            self.irAlaPortada()

                    else:
                        textLevelComplete = create_font(" Nivel " + str(self.nivel.nivel) + " Completado. Pulsa Enter para continuar ", 18, (255, 255, 255))
                        SURF.blit(textLevelComplete, ((GAME_DIMENSIONS[0] - textLevelComplete.get_width()) / 2, GAME_DIMENSIONS[1] / 2))

                        tecla_pulsada = pg.key.get_pressed()
                        if tecla_pulsada[pg.K_RETURN]:
                            self.puntosAcumulados += self.nivel.puntos
                            self.nivel = Nivel(self.nivel.get_numeroNivel() + 1, random.randint(10 * self.nivel.get_numeroNivel(), 20 * self.nivel.get_numeroNivel() ))
                            self.nave = nave(10, 275, 0)
                            self.nivel.nivelSound()

            SURF.blit(create_font("Nivel:" + str(self.nivel.nivel), 32, (255, 255, 255)),((GAME_DIMENSIONS[0] / 6) * 0, 0))
            SURF.blit(create_font("Vidas:" + str(self.vidas), 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 6) * 2, 0))
            SURF.blit(create_font("Puntos:" + str(self.puntos), 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 6) * 4, 0))

            pg.display.flip()

    def irAlaPortada(self):
        portada = True
        pg.mixer.init()
        pg.mixer.music.load("recursos/audio/intro_.ogg")
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.5)
        SPACEHEIGHT = 80
        selectOptions =[2, 1, 1]
        currentSelection = 0
        ciclos_tras_refresco = 0
        retardo_anim = 16

        while portada:
            ciclos_tras_refresco += 1
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.pantalla.blit(self.bg2, (0, 0))

            textTeclaAcceso = create_font("Presione las flechas de arriba y abajo y el espacio para acceder", 18, (255, 255, 255))
            SURF.blit(textTeclaAcceso, ((GAME_DIMENSIONS[0] - textTeclaAcceso.get_width()) / 2, GAME_DIMENSIONS[1] / 1.07))
            textTitulo = battlest.render("NAVES", 1, (255, 255, 255))
            SURF.blit(textTitulo, ((GAME_DIMENSIONS[0] - textTitulo.get_width()) / 2, GAME_DIMENSIONS[1] / 4))
            textPortada = create_font(" Jugar ", selectOptions[0] * 16, (255, 255, 255))
            SURF.blit(textPortada, ((GAME_DIMENSIONS[0] - textPortada.get_width()) / 2, textTitulo.get_rect().centery + SPACEHEIGHT * 3))
            textInstrucciones = create_font(" Instrucciones ", selectOptions[1] * 16, (255, 255, 255))
            SURF.blit(textInstrucciones, ((GAME_DIMENSIONS[0] - textInstrucciones.get_width()) / 2, textTitulo.get_rect().centery + SPACEHEIGHT * 3.75))

            tecla_pulsada = pg.key.get_pressed()
            if tecla_pulsada[pg.K_SPACE]:
                if selectOptions[0] > selectOptions[1]:
                    self.puntosAcumulados = 0
                    self.puntos = 0
                    self.vidas = VIDAS_DEL_JUEGO
                    self.nivel = Nivel(1, 30)
                    self.nave = nave(10, 275, 0)
                    portada = False
                    pg.mixer.music.stop()
                elif selectOptions[1] > selectOptions[2]:
                    self.irAlasInstrucciones()
                else:
                    self.enter_name(withName = False)

            elif tecla_pulsada[pg.K_DOWN] and currentSelection < 1 and ciclos_tras_refresco % retardo_anim == 0 :
                selectOptions[currentSelection] = 1
                selectOptions[currentSelection + 1] = 2
                currentSelection += 1
            elif tecla_pulsada[pg.K_UP] and currentSelection > 0 and ciclos_tras_refresco % retardo_anim == 0 :
                selectOptions[currentSelection] = 1
                selectOptions[currentSelection - 1] = 2
                currentSelection -= 1
            pg.display.flip()

    def irAlasInstrucciones(self):
        instrucciones= True
        SPACEHEIGHT = 80  # indice para los espacios de texto
        while instrucciones:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.pantalla.blit(self.bg3, (0, 0))

            textTitulo2 = create_font(" Instrucciones ", 50, (255, 255, 255))
            SURF.blit(textTitulo2, ((GAME_DIMENSIONS[0] - textTitulo2.get_width()) / 2, GAME_DIMENSIONS[1] - textTitulo2.get_height()* 10.5))
            textSalir = create_font("Pulse esc para volver", 18, (255, 255, 255))
            SURF.blit(textSalir, ((GAME_DIMENSIONS[0] - textSalir.get_width()) / 2, textTitulo2.get_rect().centery + SPACEHEIGHT + 450))
            textParrafos = ["Debes volar la nave por el espacio esquivando",
            "asteroides hasta llegar a un planeta donde poder aterrizar.",
            "Para pilotar la nave usa las flechas de arriba y abajo"]
            spaceProduc = 1
            for textParrafo in textParrafos:
                spaceProduc += 0.5
                textParrafoFont = create_font(textParrafo, 20, (255, 255, 255))
                SURF.blit(textParrafoFont, ((GAME_DIMENSIONS[0] - textParrafoFont.get_width()) / 2, textTitulo2.get_rect().centery + SPACEHEIGHT * spaceProduc))

            tecla_pulsada = pg.key.get_pressed()
            if tecla_pulsada[pg.K_ESCAPE]:
                instrucciones = False

            pg.display.flip()