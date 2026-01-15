import pyxel, random

# =====================
# 設定
# =====================
W, H = 21, 21          # 奇数にする（一本道迷路になる）
CELL = 6

# =====================
# 迷路生成（一本道）
# =====================
maze = [[1]*W for _ in range(H)]

def gen_maze(x, y):
    maze[y][x] = 0
    dirs = [(2,0),(-2,0),(0,2),(0,-2)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x+dx, y+dy
        if 0 < nx < W-1 and 0 < ny < H-1 and maze[ny][nx] == 1:
            maze[y+dy//2][x+dx//2] = 0
            gen_maze(nx, ny)

gen_maze(1, 1)

# =====================
# プレイヤー・ゴール
# =====================
px, py = 1, 1
goal = (W-2, H-2)
light_on = True

# =====================
# アプリ
# =====================
class App:
    def __init__(self):
        pyxel.init(W*CELL, H*CELL, title="Light Maze")
        pyxel.run(self.update, self.draw)

    def update(self):
        global px, py, light_on

        if pyxel.btnp(pyxel.KEY_SPACE):
            light_on = not light_on

        dx = pyxel.btnp(pyxel.KEY_RIGHT) - pyxel.btnp(pyxel.KEY_LEFT)
        dy = pyxel.btnp(pyxel.KEY_DOWN) - pyxel.btnp(pyxel.KEY_UP)

        nx, ny = px+dx, py+dy
        if 0 <= nx < W and 0 <= ny < H and maze[ny][nx] == 0:
            px, py = nx, ny

    def draw(self):
        pyxel.cls(0)

        cx, cy = px*CELL+CELL//2, py*CELL+CELL//2

        # 迷路＋ライト
        if light_on:
            r = 32
            for y in range(H):
                for x in range(W):
                    dx = (x*CELL+CELL//2) - cx
                    dy = (y*CELL+CELL//2) - cy
                    if dx*dx + dy*dy < r*r:
                        col = 7 if maze[y][x] else 1
                        pyxel.rect(x*CELL, y*CELL, CELL, CELL, col)
        else:
            pyxel.rect(px*CELL, py*CELL, CELL, CELL, 1)

        # ゴール
        gx, gy = goal
        pyxel.rectb(gx*CELL, gy*CELL, CELL, CELL, 8)

        # =====================
        # プレイヤー（最前面）
        # =====================
        pyxel.rect(px*CELL+1, py*CELL+1, CELL-2, CELL-2, 8)
        pyxel.rectb(px*CELL, py*CELL, CELL, CELL, 10)

        # クリア表示
        if (px, py) == goal:
            pyxel.text(5, 5, "CLEAR!", 10)

App()
