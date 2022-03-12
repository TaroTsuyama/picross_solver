from picross_solver import Picross
from datetime import datetime

horizontal_hints =[
    [2,1,1,3,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,],
    [2,1,1,3,1,1,2,1],
    [1,1,1,1,1,1,1,1,2],
    [1,1,1,1,1,1,1,1,],
]

vertical_hints = [
    [5],
    [1,1],
    [1],
    [0],
    [2],
    [3],
    [2],
    [0],
    [1],
    [5],
    [1],
    [0],
    [5],
    [1],
    [5],
    [0],
    [3],
    [1,1],
    [3],
    [0],
    [5],
    [1],
    [1],
    [5],
]

p = Picross(horizontal_hints, vertical_hints)

start = datetime.now()

p.solve()
p.show()

print(f"処理時間: {datetime.now() - start}")