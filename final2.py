# Pyxel（ゲーム用ライブラリ）と random（乱数）を読み込む
import pyxel, random

# =====================
# 基本設定
# =====================

# 迷路の横幅(W)・縦幅(H)
# 奇数にすることで、一本道の迷路が生成できる
W, H = 21, 21

# 1マスあたりのピクセルサイズ
CELL = 6

# =====================
# 迷路生成（一本道迷路）
# =====================

# 迷路データ
# 1 = 壁、0 = 通路
# 最初はすべて壁で初期化
maze = [[1]*W for _ in range(H)]

# 再帰を使った迷路生成関数
def gen_maze(x, y):
    # 現在位置を通路にする
    maze[y][x] = 0

    # 移動方向（2マスずつ動く）
    # これにより壁と通路が交互にできる
    dirs = [(2,0),(-2,0),(0,2),(0,-2)]

    # 掘る方向をランダムにする
    random.shuffle(dirs)

    # 各方向を順番に試す
    for dx, dy in dirs:
        # 次に進むマス（2マス先）
        nx, ny = x+dx, y+dy

        # ・迷路の外に出ない
        # ・まだ掘られていない壁である
        if 0 < nx < W-1 and 0 < ny < H-1 and maze[ny][nx] == 1:
            # 現在位置と次の位置の間の壁を壊す
            maze[y+dy//2][x+dx//2] = 0

            # 次のマスからさらに掘り進める（再帰）
            gen_maze(nx, ny)

# (1,1) をスタート地点として迷路を生成
gen_maze(1, 1)

# =====================
# プレイヤー・ゴール設定
# =====================

# プレイヤーの初期位置
px, py = 1, 1

# ゴール位置（右下）
goal = (W-2, H-2)

# ライトのON/OFF状態
light_on = True

# =====================
# メインアプリ
# =====================
class App:
    def __init__(self):
        # 画面サイズを設定してウィンドウを作成
        pyxel.init(W*CELL, H*CELL, title="Light Maze")

        # update（処理）と draw（描画）を毎フレーム実行
        pyxel.run(self.update, self.draw)

    # =====================
    # 更新処理（操作・判定）
    # =====================
    def update(self):
        # グローバル変数を使う宣言
        global px, py, light_on

        # Spaceキーが押されたらライトをON/OFF切り替え
        if pyxel.btnp(pyxel.KEY_SPACE):
            light_on = not light_on

        # 矢印キー入力
        # 押された方向は1、押されていない方向は0
        dx = pyxel.btnp(pyxel.KEY_RIGHT) - pyxel.btnp(pyxel.KEY_LEFT)
        dy = pyxel.btnp(pyxel.KEY_DOWN) - pyxel.btnp(pyxel.KEY_UP)

        # 次の移動先
        nx, ny = px+dx, py+dy

        # ・迷路の範囲内
        # ・通路（0）の場合のみ移動可能
        if 0 <= nx < W and 0 <= ny < H and maze[ny][nx] == 0:
            px, py = nx, ny

    # =====================
    # 描画処理
    # =====================
    def draw(self):
        # 画面を黒でクリア
        pyxel.cls(0)

        # プレイヤーの中心座標（ライト計算用）
        cx = px*CELL + CELL//2
        cy = py*CELL + CELL//2

        # =====================
        # 迷路描画（ライト処理）
        # =====================
        if light_on:
            # ライトの見える半径
            r = 32

            # 迷路全体をチェック
            for y in range(H):
                for x in range(W):
                    # 各マスの中心からプレイヤーまでの距離
                    dx = (x*CELL + CELL//2) - cx
                    dy = (y*CELL + CELL//2) - cy

                    # ライトの円の中だけ描画
                    if dx*dx + dy*dy < r*r:
                        # 壁なら明るい色、通路なら暗い色
                        col = 7 if maze[y][x] else 1
                        pyxel.rect(x*CELL, y*CELL, CELL, CELL, col)
        else:
            # ライトOFF時はプレイヤーの位置だけ見える
            pyxel.rect(px*CELL, py*CELL, CELL, CELL, 1)

        # =====================
        # ゴール描画
        # =====================
        gx, gy = goal
        # ゴールは枠線だけ表示
        pyxel.rectb(gx*CELL, gy*CELL, CELL, CELL, 8)

        # =====================
        # プレイヤー描画（最前面）
        # =====================
        # 中身
        pyxel.rect(px*CELL+1, py*CELL+1, CELL-2, CELL-2, 8)
        # 枠線
        pyxel.rectb(px*CELL, py*CELL, CELL, CELL, 10)

        # =====================
        # クリア表示
        # =====================
        if (px, py) == goal:
            pyxel.text(5, 5, "CLEAR!", 10)

# アプリ起動
App()
