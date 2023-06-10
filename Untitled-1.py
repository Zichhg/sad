from pygame import *
'''Необхідні класи'''


# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height)) #разом 55,55 - параметри
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
 
#ігрова сцена:
back = (200, 255, 255)  #колір фону (background)
win_width = 900
win_height = 800
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("g.jpg"), (win_width, win_height))

#музика
mixer.init()
mixer.music.load("musica.mp3")
mixer.music.play()
 
#прапорці, що відповідають за стан гри
game = True
finish = False
clock = time.Clock()
FPS = 60
 
#створення м'яча та ракетки  
racket1 = Player('K.png', 30, 200, 4, 40, 130) 
racket2 = Player('L.png', 720, 200, 4, 40, 130)
ball = GameSprite('M.png', 200, 200, 4, 80, 80)
 
font.init()
font1 = font.SysFont("Arial", 35)

lose1 = font1.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font1.render('PLAYER 2 LOSE!', True, (180, 0, 0))
font2 = font.SysFont("Arial", 28)
speed_x = 3
speed_y = 3
scor1 = 0
scor2 = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
  
    if finish != True:
        keys = key.get_pressed()
        window.blit(background,(0, 0))
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        text = font2.render("Рахунок 1: " + str(scor1), 1, (255, 255, 255))
        window.blit(text, (650, 10))
 
        text_lose = font2.render("Рахунок 2: " + str(scor2), 1, (255, 255, 255))
        window.blit(text_lose, (650, 40))

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
            speed_y +=1
            speed_x +=1
        #якщо м'яч досягає меж екрана, змінюємо напрямок його руху
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
    
        #якщо м'яч відлетів далі ракетки, виводимо умову програшу для першого гравця
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            finish =False
            if keys[K_r]:
                scor2 += 1 
                ball.rect.x = 300
                ball.rect.y = 250
                speed_x = 3
                speed_y = 3
    
        #якщо м'яч полетів далі ракетки, виводимо умову програшу другого гравця
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            finish =False
            if keys[K_r]:
                scor1 += 1
                ball.rect.x = 300
                ball.rect.y = 250
                speed_x = 3
                speed_y = 3

        if keys[K_y]:
            scor1 = 0
            scor2 = 0
        racket1.reset()
        racket2.reset()
        ball.reset()
    
    display.update()
    clock.tick(FPS)