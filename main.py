#!/bin/python
from random import randint
import tty
import termios
import sys

class Player:
    x=0
    y=0
    map_x=0
    map_y=0
    def move(self, x, y):
        self.x+=x
        self.y+=y

class tile:
    def __init__(self, char):
        self.char=char

class Chunk:
    tiles: list[list[tile]] = []

    def generate_chunk() -> list[list[tile]]:
        chunk: Chunk = Chunk()
        for i in range(CHUNKSIZE):
            row: list[int] = []
            for j in range(CHUNKSIZE):
                row.append();
            chunk.append(row)
        return chunk

class World:
    CHUNKSIZE: int = 16
    
    chunks: list[list[Chunk]] = []

    def __init__(self, tile_chars: list[str]):
        self.tile_chars: list[str] = tile_chars
        self.MAXTILE: int = len(tile_chars)

    def draw_chunk(self, x: int, y: int):
        for i in range(self.CHUNKSIZE):
            for j in range(self.CHUNKSIZE):
                print(self.tile_chars[self.chunks[x][y].tiles[i][j]], end="", flush=True)
            print()

def getc() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



def keyboard_handle(char: str, player: Player) -> None:
    match char:
        case 'w':
            player.move(0, -1)
        case 'a':
            player.move(-1, 0)
        case 's':
            player.move(0, 1)
        case 'd':
            player.move(1, 0)
        case 'q':
            exit(0)


def main() -> int:
    player: Player = Player()
    world: World = World(tile_chars=[",","."])
    running = True
    while running:
        input_char: str = getc()
        keyboard_handle(input_char, player)

    return 0

if __name__ == '__main__':
    exit(main())
