#Подключение нужных модулей
import pygame
from random import randint
pygame.init()


#создание окна игры
clock = pygame.time.Clock()
back = (0, 0, 0) #цвет фона (background)
mw = pygame.display.set_mode((1000, 500)) #окно программы (main window)
mw.fill(back)


#цвета
BLACK = (0, 0, 0)
LIGHT_BLUE = (200, 200, 255)


class TextArea():
   def __init__(self, x=0, y=0, width=10, height=10, color=(255, 255, 255)):
       """ область: прямоугольник в нужном месте и нужного цвета """
       #запоминаем прямоугольник:
       self.rect = pygame.Rect(x, y, width, height)
       #цвет заливки - или переданный параметр, или общий цвет фона
       self.fill_color = color


   #установить текст
   def set_text(self, text, fsize=12, text_color=BLACK):
       self.text = text
       self.image = pygame.font.Font(None, fsize).render(text, True, text_color)
      
   #отрисовка прямоугольника с текстом
   def draw(self, shift_x=0, shift_y=0):
       pygame.draw.rect(mw, self.fill_color, self.rect)
       mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))   


#создание карточек
quest_card = TextArea(120, 100, 290, 70, LIGHT_BLUE)
quest_card.set_text("Вопрос", 75)


ans_card = TextArea(120, 240, 290, 70, LIGHT_BLUE)
ans_card.set_text("Ответ", 75)


quest_card.draw(10,10)
ans_card.draw(10,10)
is_dead = False

while not is_dead:
    pygame.display.update()
    for event in pygame.event.get():
       print(event)
       if event.type == pygame.KEYDOWN:
           


           if event.key == pygame.K_q:
               num = randint(1,3)
               if num == 1:
                   quest_card.set_text('Что изучаешь в Алгоритмике?', 25)
               if num == 2:
                   quest_card.set_text('На каком языке говорят во Франции?', 25)
               if num == 3:
                   quest_card.set_text('Что растёт на яблоне?', 35)      


               quest_card.draw(10,25)


           if event.key == pygame.K_a:
               num = randint(1,3)
               if num == 1:
                   ans_card.set_text('Python', 35)
               if num == 2:
                   ans_card.set_text('Французский', 35)
               if num == 3:
                   ans_card.set_text('Яблоки', 35)      


               ans_card.draw(10, 25)
    clock.tick(40)