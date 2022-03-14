import sys
sys.setrecursionlimit(100000)# 再帰の上限を増やす

import itertools

from datetime import datetime, timedelta

from enum import Enum, auto
import copy

class CellStatus(Enum):
    """
        マスの状態を定義する列挙型クラス
    """
    VOID = auto() # 未確定マス
    FILLED = auto() # 黒マス
    BLANK = auto() # 白マス

class PicrossCell:
    """
        ピクロスのマス
    """
    def __init__(self):
        self._status = CellStatus.VOID

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status in CellStatus:
            self._status = status

class Picross:
    CELL_CHARACTER = {
        CellStatus.VOID : "＊",
        CellStatus.FILLED : "■",
        CellStatus.BLANK : "□",
    }

    def __init__(self, h_hints, v_hints):
        self._h_hints = copy.deepcopy(h_hints)
        self._v_hints = copy.deepcopy(v_hints)
        self._height = len(self.h_hints)
        self._width = len(self.v_hints)
        self._field = [[PicrossCell() for _ in range(self.width)] for _ in range(self.height)]
        self._solved = False

        self._total_h_blanks = self._get_total_blanks("horizontal")
        self._total_v_blanks = self._get_total_blanks("vertical")

    @property
    def v_hints(self):
        return self._v_hints

    @property
    def h_hints(self):
        return self._h_hints

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def field(self):
        return self._field

    def show(self):
        for line in self.field:
            print("".join([Picross.CELL_CHARACTER[cell.status] for cell in line]))

    def _check_line(self, index, direction="horizontal"):
        """
            行、または列の入力状態をチェックする
            引数
                index: int
                    行、または列のインデックス
                direction: str
                    horizontal: 行をチェック
                    vertical: 列をチェック
            戻り値
                入力状態に対してヒント数列が
                    成立する場合は True
                    成立しない場合は False
        """
        if direction == "horizontal":
            line = self._line_to_nums(self.field[index])
            hints = self.h_hints[index]
        elif direction == "vertical":
            line = self._line_to_nums(self._get_column(index))
            hints = self.v_hints[index]
        else:
            raise

        for blanks_pattern in self._blanks_pattern_generator(index, direction):
            nums = self._status_line_to_digit_line(self._get_cell_status_line(blanks_pattern, hints))
            check_line = [int(all(pair)) for pair in zip(line,nums)]

            if line == check_line:
                return True

        return False

    def _check_field(self):
        """
            全ての行の入力状態が成立するかチェック
        """
        for child_index in range(self.width):
            if not self._check_line(child_index, "vertical"):
                return False

        return True

    def _get_column(self, index):
        """
            列を取得する
        """
        return  [line[index] for line in self.field]

    def _line_to_nums(self, line):
        """
            入力状態を数値に変換する
        """
        status_line = [cell.status for cell in line]

        return [1 if status is CellStatus.FILLED else 0 for status in status_line]

    def _get_total_blanks(self, direction="horizontal"):
        """
            全行、または全列の 「BLANK となるマスの個数」 のリストを返す
        """
        ret_list = []

        if direction == "horizontal":
            for line in self.h_hints:
                ret_list.append(self.width - sum(line))

        elif direction == "vertical":
            for line in self.v_hints:
                ret_list.append(self.height - sum(line))

        return ret_list

    def _get_usable_blanks(self, index, base, direction="horizontal"):
        if direction == "horizontal":
            return self._total_h_blanks[index] - sum(base)

        elif direction == "vertical":
            return self._total_v_blanks[index] - sum(base)

    def _blanks_pattern_generator(self, index, direction="horizontal", base=None, child_index=0):
        """
            ヒント数字に対して 「BLANK の個数」 の全てのパターンを導出するジェネレータ
        """
        if base == None:
            base = self._get_blanks_base(index,direction)

        for i in range(self._get_usable_blanks(index, base, direction)+1):
            blanks = base.copy()
            blanks[child_index] += i

            if child_index == len(base)-1:
                blanks[child_index] = self._get_usable_blanks(index, blanks, direction)
                yield blanks
                return

            yield from self._blanks_pattern_generator(index, direction, blanks, child_index+1)

    def _get_blanks_base(self, index, direction="horizontal"):
        """
            要素数がヒント数列の要素数 +1 かつ、先頭および末尾が 0 でそれ以外が 1 のリストを返す
                ex.)
                    ヒント数列 = [1,2,3] のときの戻り値
                        → [0,1,1,0]
            ヒント数列の数字間には BLANK となるマスが必ず 1 つ以上入るため
        """
        if direction == "horizontal":
            return [0 if i in (0,len(self.h_hints[index])) else 1 for i in range(len(self.h_hints[index])+1)]

        elif direction == "vertical":
            return [0 if i in (0,len(self.v_hints[index])) else 1 for i in range(len(self.v_hints[index])+1)]

    def _join_blanks_and_hints(self, blanks, hints):
        """
            「BLANK の個数」 と 「FILLED の個数」 を交互に列挙した数列を返す
        """
        tmp_hints = hints.copy()
        tmp_hints.append(None)
        return list(itertools.chain.from_iterable(zip(blanks, tmp_hints)))[:-1]

    def _get_cell_status_line(self, blanks, hints):
        """
            「BLANK の個数」 と 「FILLED の個数」 を交互に列挙した数列を CellStatus に変換する
        """
        nums = self._join_blanks_and_hints(blanks, hints)
        return list(itertools.chain.from_iterable([[CellStatus.BLANK for _ in range(num)] if index%2 == 0 else [CellStatus.FILLED for _ in range(num)] for index,num in enumerate(nums)]))

    def _status_line_to_digit_line(self, status_line):
        return [1 if status is CellStatus.FILLED else 0 for status in status_line]

    def _set_line(self, index, blanks_pattern=None):
        """
            行を入力する
        """
        if blanks_pattern == None: # blanks_pattern が None の場合 index 以下をリセット
            for i in range(index,self.height):
                for cell in self.field[i]:
                    cell.status = CellStatus.VOID
        else:
            line = self._get_cell_status_line(blanks_pattern, self.h_hints[index])
            for child_index in range(len(self.field[index])):
                self.field[index][child_index].status = line[child_index]

    def _is_confirmed(self):
        """
            フィールドに未確定のマスがないかチェック
        """
        return all([line.status != CellStatus.VOID for row in self.field for line in row])

    def _disp_message(func):
        start = datetime.now()
        count = 0
        print("solving", end="\r")
        def inner(*args):
            nonlocal start
            nonlocal count
            if datetime.now() - start >= timedelta(seconds=1):
                start = datetime.now()
                count += 1
                if count > 3:
                    count = 0
                    print(" "*50, end="\r")
                print("solving"+"."*count, end="\r")
            return func(*args)
        return inner

    @_disp_message
    def solve(self, index=0):
        """
            再帰で解く
        """
        check = False
        check_ng = False
        if index < len(self.h_hints):

            for blanks_pattern in self._blanks_pattern_generator(index):
                self._set_line(index, blanks_pattern)

                if self._check_field():
                    if self._is_confirmed():
                        self._solved = True
                        return

                    self.solve(index+1)
                    if self._solved:
                        return

                self._set_line(index) # index 以下をリセット

