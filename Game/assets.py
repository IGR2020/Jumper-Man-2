import pygame as pg
from Game.functions import *

version = "Beta-2"
levelLocation = "Game/Levels/"

blockSize = 96
playerSize = 64
assets = load_assets("Game/Assets/Terrain", (blockSize, blockSize))
assets["Virtual Guy"] = load_sprite_sheets(r"Game\Assets\Main Characters\Virtual Guy", 32, 32, resize=(playerSize, playerSize), direction=True)
assets["Mask Dude"] = load_sprite_sheets(r"Game\Assets\Main Characters\Mask Dude", 32, 32, resize=(playerSize, playerSize), direction=True)
assets["Ninja Frog"] = load_sprite_sheets(r"Game\Assets\Main Characters\Ninja Frog", 32, 32, resize=(playerSize, playerSize), direction=True)
assets["Pink Man"] = load_sprite_sheets(r"Game\Assets\Main Characters\Pink Man", 32, 32, resize=(playerSize, playerSize), direction=True)

# background
backgroundSize = 128
assets["Background"] = load_assets("Game/Assets/Background", scale=2)

# loading traps
spikeSize = 64, 64
fireSize = 16, 32
assets["Spike"] = load(r"Game\Assets\Traps\Spikes\Idle.png", spikeSize, 1)
assets["Fire"] = load_sprite_sheets(r"Game\Assets\Traps\Fire", fireSize[0], fireSize[1], False)