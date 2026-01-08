import pyxel, random

W,H = 20,20
CELL = 6

maze = [[1]*W for _ in range(H)]

def gen_maze(x, y):
    maze[y][x] = 0
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x+dx*2, y+dy*2
        if 0<=nx<W and 0<=ny<H and maze[ny][nx]==1:
            maze[y+dy][x+dx] = 0
            gen_maze(nx, ny)

gen_maze(1,1)

px, py = 1,1
goal = (W-2,H-2)
light_on = True

class App:
    def __init__(self):
        pyxel.init(W*CELL, H*CELL, title="Light Maze")
        pyxel.run(self.update, self.draw)

    def update(self):
        global px, py, light_on
        if pyxel.btnp(pyxel.KEY_SPACE):
            light_on = not light_on

        dx = pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)
        dy = pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP)
        nx, ny = px+dx, py+dy
        if 0<=nx<W and 0<=ny<H and maze[ny][nx]==0:
            px, py = nx, ny

    def draw(self):
        pyxel.cls(0)
        cx, cy = px*CELL+CELL//2, py*CELL+CELL//2

        # ライトON → ノイズ入りの円形ライト
        if light_on:
            base_r = 30
            r = base_r + random.randint(-2,2)

            for y in range(H):
                for x in range(W):
                    wx, wy = x*CELL, y*CELL
                    dx = (wx+CELL//2 - cx)
                    dy = (wy+CELL//2 - cy)
                    if dx*dx + dy*dy < r*r:
                        col = 7 if maze[y][x]==1 else 1
                        pyxel.rect(wx, wy, CELL, CELL, col)

        # ライトOFF → 自分の位置だけ少し見える
        else:
            pyxel.rect(px*CELL, py*CELL, CELL, CELL, 3)

        # ゴール（光の有無に関係なく見えてOKにしたい場合）
        gx, gy = goal
        pyxel.rectb(gx*CELL, gy*CELL, CELL, CELL, 8)

App()
