# 最終課題-メイン で使用する Python ソースファイルです
# --------------------------
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

# --------------------------
@dataclass
class Maze:
    height: int = field(init = False, default = None)
    width: int = field(init = False, default = None)
    floormap: list = field(init = False, default = None)
    
    def from_file(self, filename):
        self.floormap = []
        row_list = []
        with open(filename, encoding="utf-8") as file:
            first_line = file.readline().rstrip("\n")
            values = first_line.split(",")
            self.height = values[0]
            self.width = values[1]
            for line in file:
                for value in line:
                    if value != "\n":
                        row_list.append(int(value))
                    else:
                        self.floormap.append(row_list)
                        row_list = []
