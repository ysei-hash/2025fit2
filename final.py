import pyxel, random

# --- 定数 ---
W, H = 21, 21   # ★必ず奇数
CELL = 8
VIEW = 11

# --- 迷路初期化（全部壁）---
maze = [[1 for _ in range(W)] for _ in range(H)]

# --- 完全迷路生成（DFS）---
def gen_maze(x, y):
    maze[y][x] = 0
    dirs = [(2,0), (-2,0), (0,2), (0,-2)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 < nx < W-1 and 0 < ny < H-1 and maze[ny][nx] == 1:
            maze[y + dy//2][x + dx//2] = 0
            gen_maze(nx, ny)

# スタートは必ず通路
gen_maze(1, 1)

# --- 状態 ---
px, py = 1, 1
goal = (W-2, H-2)  # ★必ず通路になる

class App:
    def __init__(self):
        pyxel.init(VIEW*CELL, VIEW*CELL, title="One-Path Light Maze")
        pyxel.run(self.update, self.draw)

    def update(self):
        global px, py
        dx = dy = 0
        if pyxel.btnp(pyxel.KEY_RIGHT): dx = 1
        if pyxel.btnp(pyxel.KEY_LEFT):  dx = -1
        if pyxel.btnp(pyxel.KEY_DOWN):  dy = 1
        if pyxel.btnp(pyxel.KEY_UP):    dy = -1

        nx, ny = px + dx, py + dy
        if 0 <= nx < W and 0 <= ny < H and maze[ny][nx] == 0:
            px, py = nx, ny

    def draw(self):
        pyxel.cls(0)
        half = VIEW // 2

        # --- カメラ追従描画 ---
        for y in range(VIEW):
            for x in range(VIEW):
                mx = px + x - half
                my = py + y - half
                if 0 <= mx < W and 0 <= my < H:
                    col = 7 if maze[my][mx] else 1
                    pyxel.rect(x*CELL, y*CELL, CELL, CELL, col)

        # --- ゴール ---
        gx, gy = goal
        if abs(px-gx)+abs(py-gy) < half:
            x = (gx-px+half)*CELL
            y = (gy-py+half)*CELL
            pyxel.rectb(x, y, CELL, CELL, 10)

        # --- プレイヤー ---
        pyxel.circ(
            half*CELL + CELL//2,
            half*CELL + CELL//2,
            CELL//2 + 1,
            11
        )

App()
