#!/bin/python
from random import randint
import random
from pygame import Color
import pygame
import time
from enum import Enum

LegacyKB = False

solid_path = "textures/items/solid/"
gas_path = "textures/items/gas/"
liquid_path = "textures/items/liquid/"
edible_path = "textures/items/food/"
textures_solid = []
textures_solid.append(pygame.image.load(solid_path+"log.png"))
textures_solid.append(pygame.image.load(solid_path+"sand.png"))
textures_solid.append(pygame.image.load(solid_path+"stick.png"))
textures_solid.append(pygame.image.load(solid_path+"stone.png"))
textures_gas = []
textures_gas.append(pygame.image.load(gas_path+"gas.png"))
textures_liquid = []
textures_liquid.append(pygame.image.load(liquid_path+"water.png"))
textures_edible = []
textures_edible.append(pygame.image.load(edible_path+"cherry.png"))
textures_edible.append(pygame.image.load(edible_path+"pumpkin.png"))
textures_edible.append(pygame.image.load(edible_path+"watermelon.png"))

BASE_ELEMENTS=100

class forms(Enum):
    SOLID=(0, "solid")
    LIQUID=(1, "liquid")
    GAS=(2, "gas")
    def __init__(self, code, description):
        self.code = code
        self.description = description
class Tile:
    def __init__(self, color):
        self.color=color

class Edible:
    def __init__(self):
        self.calories = randint(10, 500)
        self.irrigation = randint(10, 500)
        if (randint(0,100)<40):
            self.poison = randint(200, 1000)

class BaseElement:
    def name_gen(self) -> str:
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        
        length = randint(2, 6)        

        word = []
        for i in range(length):
            if i % 2 == 0:
                word.append(random.choice(vowels))
            else:
                word.append(random.choice(consonants))
        
        return ''.join(word)

    def __init__(self):
        self.form = random.choice(list(forms))
        self.name = self.name_gen()
        if self.form == forms.SOLID:
            self.texture = random.choice(textures_solid)
        if self.form == forms.GAS:
            self.texture = random.choice(textures_gas)
        if self.form == forms.LIQUID:
            self.texture = random.choice(textures_liquid)
        if (randint(0, 100) < 25):
            self.edible = Edible()
            self.texture = random.choice(textures_edible)

base_elements: list[BaseElement] = []
for i in range(BASE_ELEMENTS):
    base_elements.append(BaseElement())

class Item:
    def __init__(self, x:int, y:int, in_inventory:bool):
        self.base_element = base_elements[randint(0,BASE_ELEMENTS-1)]
        self.x=x
        self.y=y
        self.in_inventory=in_inventory
    def show(self):
        base_element = self.base_element.name
        print(f'{base_element=}')
        form = self.base_element.form.description
        print(f'{form=}')
        if hasattr(item.base_element, 'edible'):
            print("*** Edible ***")
            calories = self.base_element.edible.calories
            irrigation = self.base_element.edible.irrigation
            print(f'    {calories=}')
            print(f'    {irrigation=}')
            if hasattr(item.base_element.edible, "poison"):
                print("    *** Poison ***")
                poison = self.base_element.edible.poison
                print(f'        {poison=}')

class Chunk:
    tiles: list[list[Tile]] = []
    items: list[Item] = []
    def __init__(self, CHUNKSIZE: int):
        self.tiles = [[Tile((randint(0, 255), randint(0, 255), randint(0, 255))) for _ in range(CHUNKSIZE)] for _ in range(CHUNKSIZE)]
        self.items = [Item(randint(0,CHUNKSIZE-1), randint(0,CHUNKSIZE-1), False) for _ in range(CHUNKSIZE//2)]



class World:
    chunks = {}

    def __init__(self, chunk_size: int):
        self.CHUNKSIZE: int = chunk_size
    
    def generate_chunk(self, x:int, y:int):
        if (x, y) not in self.chunks:
            self.chunks[(x, y)] = Chunk(self.CHUNKSIZE)

class Player:
    inventory: list[Item] = []
    selected_inventory: int = 0
    irrigation: int = 500
    saturation: int = 500
    going_right=True
    def __init__(self):
        self.x=0
        self.y=0
        self.map_x=0
        self.map_y=0
    def move(self, x:int, y:int, world:World):
        self.irrigation-=3
        self.saturation-=3
        new_x=self.x+x
        new_y=self.y+y

        if new_x==world.CHUNKSIZE:
            self.map_x+=1
            self.x=0

        elif new_x==-1:
            self.map_x-=1
            self.x=world.CHUNKSIZE-1

        elif new_y==world.CHUNKSIZE:
            self.map_y+=1
            self.y=0

        elif new_y==-1:
            self.map_y-=1
            self.y=world.CHUNKSIZE-1

        else:
            self.x=new_x
            self.y=new_y
        
running = True
pygame.init()
pygame.font.init()
screensize=720
statusbar=40
info=400

screen = pygame.display.set_mode((screensize+info, screensize+statusbar))
pygame.display.set_caption("pime: python")
clock = pygame.time.Clock()
player: Player = Player()
world: World = World(chunk_size=16)
dt=1

def get_item_at_ppos() -> Item:
    for item in chunk.items:
        if (item.x == player.x) and (item.y == player.y):
            return item
    return None

playerr=pygame.image.load("textures/player/playerr.png")
playerl=pygame.image.load("textures/player/playerl.png")

sneak_texture=pygame.image.load("textures/gui/sneak_icon.png")
run_texture=pygame.image.load("textures/gui/run_icon.png")

font=pygame.font.Font("nerdfont.otf",32)
last_move_time = 0
status=""
world.generate_chunk(player.map_x, player.map_y)

# main
while running:
    keys=pygame.key.get_pressed()
  
    # player interact
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SEMICOLON:
                if len(player.inventory):
                    item = player.inventory[player.selected_inventory]
                    item.show()
            if event.key == pygame.K_f:
                if len(player.inventory) and hasattr(player.inventory[player.selected_inventory].base_element, "edible"):
                    edible=player.inventory[player.selected_inventory].base_element.edible
                    player.saturation+=edible.calories
                    player.irrigation+=edible.irrigation

                    if hasattr(edible, "poison"):
                        player.saturation-=edible.poison
                        player.irrigation-=edible.poison

                    player.inventory.remove(player.inventory[player.selected_inventory])
                    if player.selected_inventory > 0:
                        player.selected_inventory-=1
            if event.key == pygame.K_q:
                if len(player.inventory):
                    player.inventory[player.selected_inventory].x = player.x
                    player.inventory[player.selected_inventory].y = player.y
                    world.chunks.get((player.map_x, player.map_y)).items.append(player.inventory[player.selected_inventory])
                    player.inventory.remove(player.inventory[player.selected_inventory])
            if event.key == pygame.K_TAB: 
                if player.selected_inventory<(len(player.inventory)-1):
                    player.selected_inventory+=1
                else:
                    player.selected_inventory=0
            if event.key == pygame.K_BACKQUOTE:
                if player.selected_inventory>0:
                    player.selected_inventory-=1 
                else:
                    player.selected_inventory=len(player.inventory)-1

            if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                for item in chunk.items:
                    if (item.x == player.x) and (item.y == player.y):
                        player.inventory.append(item)
                        world.chunks.get((player.map_x, player.map_y)).items.remove(item)
                        break

            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_i:
                print("\n\n\n")
                for item in player.inventory:
                    item.show()
            if LegacyKB:
                match event.key:
                    case pygame.K_w:
                        player.move(0, -1, world)
                    case pygame.K_s:
                        player.move(0, 1, world)
                    case pygame.K_a:
                        player.move(-1, 0, world)
                        player.going_right = False
                    case pygame.K_d:
                        player.going_right = True
                        player.move(1, 0, world)

    # move interact
    time_period = 0.1
    sneak = False
    run = False
    if keys[pygame.K_LSHIFT]:
        time_period = 0.2
        sneak = True
    elif keys[pygame.K_LCTRL]:
        time_period = 0.05
        run = True


    current_time = time.time()
    if current_time - last_move_time >= time_period:

        if keys[pygame.K_w]:
            player.move(0, -1, world)
            last_move_time = current_time

        if keys[pygame.K_s]:
            player.move(0, 1, world)
            last_move_time = current_time

        if keys[pygame.K_a]:
            player.move(-1, 0, world)
            last_move_time = current_time
            player.going_right=False

        if keys[pygame.K_d]:
            player.going_right=True
            last_move_time = current_time
            player.move(1, 0, world)
            

    if keys[pygame.K_h]:
        print("wasd - move")
        print("q - quit")

    screen.fill("black")

    # draw
    world.generate_chunk(player.map_x, player.map_y)
    chunk = world.chunks.get((player.map_x,player.map_y))

    tile_size = screensize / world.CHUNKSIZE

    for i in range(world.CHUNKSIZE):
        for j in range(world.CHUNKSIZE):
            color = chunk.tiles[i][j].color
            tileplace_x = i * tile_size
            tileplace_y = j * tile_size
            rect = pygame.Rect(tileplace_x, tileplace_y, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)

    for item in chunk.items:
        texture = item.base_element.texture
        x = item.x * tile_size
        y = item.y * tile_size
        texture_scaled = pygame.transform.scale(texture, (tile_size, tile_size))
        screen.blit(texture_scaled, (x, y))

    if player.going_right:
        playerr_scaled = pygame.transform.scale(playerr, (tile_size, tile_size))
        screen.blit(playerr_scaled, (player.x*tile_size, player.y*tile_size))
    else:
        playerl_scaled = pygame.transform.scale(playerl, (tile_size, tile_size))
        screen.blit(playerl_scaled, (player.x*tile_size, player.y*tile_size))
    
    if run:
        run_texture_scaled = pygame.transform.scale(run_texture, (tile_size*1.5, tile_size*1.5))
        screen.blit(run_texture_scaled, (screensize-tile_size*1.5, 0))
    elif sneak:
        sneak_texture_scaled = pygame.transform.scale(sneak_texture, (tile_size*1.5, tile_size*1.5))
        screen.blit(sneak_texture_scaled, (screensize-tile_size*1.5, 0))

    status_text = font.render(status, True, Color(255,255,255,255))
    status_text_rect = (0,screensize)
    screen.blit(status_text,status_text_rect)
   
    line = 0
    text = font.render(f"x, y = {player.x}, {player.y}", True, Color(255,255,255,255))
    text_rect = (screensize, 40*line)
    screen.blit(text,text_rect)
    line += 1
    text = font.render(f"map x, y = {player.map_x}, {player.map_y}", True, Color(255,255,255,255))
    text_rect = (screensize, 40*line)
    screen.blit(text,text_rect)
    line += 1
    text = font.render(f"over x, y = {player.map_x*world.CHUNKSIZE+player.x}, {player.map_y*world.CHUNKSIZE+player.y}", True, Color(255,255,255,255))
    text_rect = (screensize, 40*line)
    screen.blit(text,text_rect)

    line += 1
    text = font.render(f"saturation = {player.saturation}", True, Color(255,255,255,255))
    text_rect = (screensize, 40*line)
    screen.blit(text,text_rect)
    
    line += 1
    text = font.render(f"irrigation = {player.irrigation}", True, Color(255,255,255,255))
    text_rect = (screensize, 40*line)
    screen.blit(text,text_rect)

    line += 1
    if get_item_at_ppos():
        text = font.render(f"item: {get_item_at_ppos().base_element.form.description} ({get_item_at_ppos().base_element.name})", True, Color(255,255,255,255))
        text_rect = (screensize, 40*line)
        screen.blit(text,text_rect)
            
    for i in range(len(player.inventory)):
        if ((i%8) == 0) and i > 0:
            line +=1

        if i!=player.selected_inventory:
            color = Color(200,200,200,255)
        else:
            color = Color(0, 200, 0, 255)

        x = screensize+tile_size*(i%8)
        y = line*50
        rect = pygame.Rect(x, y, tile_size, tile_size)
        pygame.draw.rect(screen, color, rect, 2)
        texture = player.inventory[i].base_element.texture
        texture_scaled = pygame.transform.scale(texture, (tile_size, tile_size))
        screen.blit(texture_scaled, (x, y))       

    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.font.quit()
pygame.quit()

