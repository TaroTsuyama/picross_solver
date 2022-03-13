from picross_solver import Picross
from datetime import datetime

horizontal_hints =[
    [4],
    [6],
    [2,2],
    [2,2],
    [2,2],
    [2,2],
    [2,2],
    [2,4],
    [7],
    [4,2],
]

vertical_hints = [
    [0],
    [6],
    [8],
    [2,2],
    [2,2],
    [2,3],
    [2,3],
    [8],
    [8],
    [1],
]

p = Picross(horizontal_hints, vertical_hints)

start = datetime.now()

p.solve()
p.show()

print(f"処理時間: {datetime.now() - start}")