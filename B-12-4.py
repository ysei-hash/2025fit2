import pyxel

pyxel.init(200, 200)
pyxel.cls(7)

for i in range(0, 200, 10):
    pyxel.line(0, i, i, 199, 0)

pyxel.show()

