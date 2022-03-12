from picross_solver import Picross
from datetime import datetime

horizontal_hints = [
    [1],
    [5],
    [3],
    [1,1],
    [1,1],
]

vertical_hints = [
    [1,1],
    [3],
    [3],
    [3],
    [1,1],
]


p = Picross(horizontal_hints, vertical_hints)

start = datetime.now()

p.solve()
p.show()

print(f"処理時間: {datetime.now() - start}")