import pygame

FPS = 60

WIN_HEIGHT = 800
WIN_WIDTH = 800
GAME_TITLE = 'Hurricane - INDEV'

PLAYER_IMAGE = 'data/images/entities/player/player.png'

BACKGROUND_IMAGE = 'data/images/background.png'

PISTOL_IMAGE = 'data/images/weapons/Pistol.png'
SHOTGUN_IMAGE = 'data/images/weapons/shotgun.png'
MACHINE_GUN_IMAGE = 'data/images/weapons/Rifle.png'

UI_IMAGE = 'data/images/UI.png'

PLAYER_SPEED = 4
BULLET_ACCURACY = 6
BULLET_TRAVEL_SPEED = 15
FIRE_RATE = 10
BULLET_SIZE = 7.5

MAX_PLAYER_HEALTH = 40
player_health = 40
player_invincibility_frames = 0
invincibility_duration = 30


HIT_SHAKE_INTENSITY = 3
ENEMY_DESTROY_SHAKE_INTENSITY = 20

PARTICLE_RANGE = 0.5
MUZZLE_PARTICLE_RANGE = 1

BULLET_COLOR = (255, 255, 255)

workbench_x = 700
workbench_y = 400

WAVE_INTERVAL = 300

BASE_ENEMY_HEALTH = 70
BASE_ENEMY_MOVE_SPEED = 2
ENEMY_KNOCKBACK = 4

NORTH_FRAME1 = 'data/images/entities/player/north/northframe1.png'
NORTH_FRAME2 = 'data/images/entities/player/north/northframe2.png'
NORTH_FRAME3 = 'data/images/entities/player/north/northframe1.png'
NORTH_FRAME4 = 'data/images/entities/player/north/northframe3.png'

EAST_FRAME1 = 'data/images/entities/player/east/eastframe1.png'
EAST_FRAME2 = 'data/images/entities/player/east/eastframe2.png'
EAST_FRAME3 = 'data/images/entities/player/east/eastframe1.png'
EAST_FRAME4 = 'data/images/entities/player/east/eastframe3.png'

SOUTH_FRAME1 = 'data/images/entities/player/south/southframe1.png'
SOUTH_FRAME2 = 'data/images/entities/player/south/southframe2.png'
SOUTH_FRAME3 = 'data/images/entities/player/south/southframe1.png'
SOUTH_FRAME4 = 'data/images/entities/player/south/southframe3.png'

WEST_FRAME1 = 'data/images/entities/player/west/westframe1.png'
WEST_FRAME2 = 'data/images/entities/player/west/westframe2.png'
WEST_FRAME3 = 'data/images/entities/player/west/westframe1.png'
WEST_FRAME4 = 'data/images/entities/player/west/westframe3.png'

player_direction = "south"
player_frame = 0

player_speed = PLAYER_SPEED
animation_speed = 8

weapon_length = 65
gun_pivot_offset = (-5, 10)
gun_kickback_distance = 4
gun_kickback_speed = 2
gun_kickback = 0

shoot_delay = FIRE_RATE
bullet_accuracy = BULLET_ACCURACY
bullet_speed = BULLET_TRAVEL_SPEED

bullets = []
particle_systems = []

