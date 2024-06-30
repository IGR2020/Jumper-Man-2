from EPT import load_sprite_sheets

# initializing assets/levels/characters
block_size = 32*2
assets = load_sprite_sheets("Assets", 16, 16, 1, False, (block_size, block_size))
player_size = 32*2