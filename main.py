#!/bin/python
from random import randint
import tty
import termios
import sys

class tile:
    def __init__(self, char):
        self.char=char

class Chunk:
    tiles: list[list[tile]] = []

    def __init__(self, tile_chars: list[str], MAXTILE: int, CHUNKSIZE: int):
        for i in range(CHUNKSIZE):
            row: list[int] = []
            for j in range(CHUNKSIZE):
                row.append(tile_chars[randint(0, MAXTILE)]);
            self.tiles.append(row)

class World:
    chunks: list[list[Chunk]] = []

    def __init__(self, tile_chars: list[str], world_size: int, chunk_size: int):
        self.CHUNKSIZE: int = chunk_size
        self.MAXTILE: int = len(tile_chars)-1

        self.tile_chars: list[str] = tile_chars
        self.world_size: int = world_size

        for i in range(self.world_size):
            row: list[Chunk] = []
            for j in range(self.world_size):
                row.append(Chunk(tile_chars=self.tile_chars, MAXTILE=self.MAXTILE, CHUNKSIZE=self.CHUNKSIZE))
            self.chunks.append(row)

    def draw_chunk(self, x: int, y: int):
        for i in range(self.CHUNKSIZE):
            for j in range(self.CHUNKSIZE):
                print(self.chunks[x][y].tiles[i][j], end="", flush=True)
            print()


class Player:
    def __init__(self):
        self.x=0
        self.y=0
        self.map_x=0
        self.map_y=0
    def move(self, x:int, y:int, world:World):
        new_x=self.x+x
        new_y=self.y+y
        if new_x==world.CHUNKSIZE:
            self.map_x+=1
            self.x=0
        elif new_x==-1:
            self.map_x-=1
            self.x=world.CHUNKSIZE-1
        elif new_y==world.CHUNKSIZE-1:
            self.map_y+=1
            self.y=0
        elif new_y==-1:
            self.map_y-=1
            self.y=world.CHUNKSIZE-2
        else:
            self.x=new_x
            self.y=new_y
        



def getc() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



def keyboard_handle(char: str, player: Player, world: World) -> None:
    match char:
        case 'w':
            player.move(0, -1, world)
        case 'a':
            player.move(-1, 0, world)
        case 's':
            player.move(0, 1, world)
        case 'd':
            player.move(1, 0, world)
        case 'q':
            exit(0)
        case 'h':
            print("wasd - move")
            print("q - quit")
            print("e - draw")


def main() -> int:
    player: Player = Player()
    world: World = World(tile_chars=[",","."], world_size=16, chunk_size=32)
    running = True
    while running:
        print("\n"*50)
        print("\033[0;0;H", end="")
        world.draw_chunk(player.map_x, player.map_y);
        print(f"\033[{player.y+2};{player.x+1}H", end='')
        print("@", end='')
        print("\033[100;100;H", end="")
        print()
        input_char: str = getc()
        keyboard_handle(input_char, player, world)
    return 0

if __name__ == '__main__':
    exit(main())
