import pyxel
import math

FIELD_SIZE = 150

class Ball:
    speed = 1
    
    def __init__(self, field_size):
        self.field_size = field_size
        self.restart()
        
    def move(self):
        self.x += self.vx * Ball.speed
        self.y += self.vy * Ball.speed
        if (self.x < 0) or (self.x >= self.field_size):
            self.vx = -self.vx
            
    def restart(self):
        self.x = pyxel.rndi(0, self.field_size - 1)
        self.y = 0
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

class Pad:
    def __init__(self, field_size):
        self.field_size = field_size
        self.x = self.field_size / 2
        self.size = self.field_size / 5
        
    def catch(self, ball):
        if ball.y >= self.field_size - self.field_size / 40 and \
           (self.x - self.size / 2 <= ball.x <= self.x + self.size / 2):
            pyxel.play(0, 0)
            ball.restart()
            return True
        else:
            return False

class App:
    def __init__(self):
        self.field_size = FIELD_SIZE
        pyxel.init(self.field_size, self.field_size)
        
        pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
        pyxel.sound(1).set(notes='C2', tones='N', volumes='3', effects='S', speed=30)
        
        self.balls = [Ball(self.field_size)]
        self.pad = Pad(self.field_size)
        self.alive = True
        self.life = 10
        self.receive = 0
        self.score = 0
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.alive:
            return
        
        self.pad.x = pyxel.mouse_x
        
        for b in self.balls:
            b.move()
            
            if self.pad.catch(b):
                Ball.speed += 0.2
                self.score += 1
                self.receive += 1
                
                if self.receive >= 10:
                    Ball.speed = 1
                    self.receive = 0
                    self.balls.append(Ball(self.field_size))
            
            elif b.y >= self.field_size:
                pyxel.play(0, 1)
                b.restart()
                Ball.speed += 0.2
                self.life -= 1
                self.alive = (self.life > 0)
                
    def draw(self):
        if self.alive:
            pyxel.cls(7)
            
            for b in self.balls:
                pyxel.circ(b.x, b.y, self.field_size/20, 6)
                
            pyxel.rect(self.pad.x - self.pad.size / 2, 
                       self.field_size - self.field_size / 40, 
                       self.pad.size, 
                       5, 
                       14)
                       
            pyxel.text(5, 5, "score: " + str(self.score), 0)
            pyxel.text(5, 15, "life: " + str(self.life), 0)
        else:
            pyxel.cls(0)
            text = "Game Over!!! Score: " + str(self.score)
            text_x = self.field_size / 2 - len(text) * 2
            pyxel.text(text_x, self.field_size / 2 - 4, text, 7)

if __name__ == "__main__":
    App()
