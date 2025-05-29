import pygame

images = {}
sounds = {}

def load_assets():
    # --- Samurai1 ---
    images['samurai1_ATTACK1'] = pygame.image.load("assets/images/character/samurai1/Sprites/ATTACK1.png").convert_alpha()
    images['samurai1_ATTACK2'] = pygame.image.load("assets/images/character/samurai1/Sprites/ATTACK2.png").convert_alpha()
    images['samurai1_ATTACK3'] = pygame.image.load("assets/images/character/samurai1/Sprites/ATTACK3.png").convert_alpha()
    images['samurai1_DEATH'] = pygame.image.load("assets/images/character/samurai1/Sprites/DEATH.png").convert_alpha()
    images['samurai1_DEFEND'] = pygame.image.load("assets/images/character/samurai1/Sprites/DEFEND.png").convert_alpha()
    images['samurai1_HEALING'] = pygame.image.load("assets/images/character/samurai1/Sprites/HEALING.png").convert_alpha()
    images['samurai1_HURT'] = pygame.image.load("assets/images/character/samurai1/Sprites/HURT.png").convert_alpha()
    images['samurai1_idle'] = pygame.image.load("assets/images/character/samurai1/Sprites/idle.png").convert_alpha()
    images['samurai1_JUMP'] = pygame.image.load("assets/images/character/samurai1/Sprites/JUMP.png").convert_alpha()
    images['samurai1_jumpfall'] = pygame.image.load("assets/images/character/samurai1/Sprites/jumpfall.png").convert_alpha()
    images['samurai1_RUN'] = pygame.image.load("assets/images/character/samurai1/Sprites/RUN.png").convert_alpha()
    images['samurai1_THROW'] = pygame.image.load("assets/images/character/samurai1/Sprites/THROW.png").convert_alpha()
    images['samurai1_ultimate'] = pygame.image.load("assets/images/character/samurai1/Sprites/ultimate.png").convert_alpha()

    # --- Samurai2 ---
    images['samurai2_ATTACK1'] = pygame.image.load("assets/images/character/samurai2/Sprites/ATTACK1.png").convert_alpha()
    images['samurai2_ATTACK2'] = pygame.image.load("assets/images/character/samurai2/Sprites/ATTACK2.png").convert_alpha()
    images['samurai2_ATTACK3'] = pygame.image.load("assets/images/character/samurai2/Sprites/ATTACK3.png").convert_alpha()
    images['samurai2_DEATH'] = pygame.image.load("assets/images/character/samurai2/Sprites/DEATH.png").convert_alpha()
    images['samurai2_defend'] = pygame.image.load("assets/images/character/samurai2/Sprites/defend.png").convert_alpha()
    images['samurai2_DUSTEFFECT'] = pygame.image.load("assets/images/character/samurai2/Sprites/DUST EFFECT.png").convert_alpha()
    images['samurai2_HURT'] = pygame.image.load("assets/images/character/samurai2/Sprites/HURT.png").convert_alpha()
    images['samurai2_IDLE'] = pygame.image.load("assets/images/character/samurai2/Sprites/IDLE.png").convert_alpha()
    images['samurai2_JUMP'] = pygame.image.load("assets/images/character/samurai2/Sprites/JUMP.png").convert_alpha()
    images['samurai2_RUN'] = pygame.image.load("assets/images/character/samurai2/Sprites/RUN.png").convert_alpha()
    images['samurai2_THROW'] = pygame.image.load("assets/images/character/samurai2/Sprites/THROW.png").convert_alpha()
    images['samurai2_ultimate'] = pygame.image.load("assets/images/character/samurai2/Sprites/ultimate.png").convert_alpha()

    # --- Samurai3 ---
    images['samurai3_ATTACK1'] = pygame.image.load("assets/images/character/samurai3/Sprites/ATTACK1.png").convert_alpha()
    images['samurai3_ATTACK2'] = pygame.image.load("assets/images/character/samurai3/Sprites/ATTACK2.png").convert_alpha()
    images['samurai3_ATTACK3'] = pygame.image.load("assets/images/character/samurai3/Sprites/ATTACK3.png").convert_alpha()
    images['samurai3_DEATH'] = pygame.image.load("assets/images/character/samurai3/Sprites/DEATH.png").convert_alpha()
    images['samurai3_THROW'] = pygame.image.load("assets/images/character/samurai3/Sprites/THROW.png").convert_alpha()
    images['samurai3_HURT'] = pygame.image.load("assets/images/character/samurai3/Sprites/HURT.png").convert_alpha()
    images['samurai3_IDLE'] = pygame.image.load("assets/images/character/samurai3/Sprites/IDLE.png").convert_alpha()
    images['samurai3_JUMP'] = pygame.image.load("assets/images/character/samurai3/Sprites/JUMP.png").convert_alpha()
    images['samurai3_RUN'] = pygame.image.load("assets/images/character/samurai3/Sprites/RUN.png").convert_alpha()
    images['samurai3_ultimate'] = pygame.image.load("assets/images/character/samurai3/Sprites/ultimate.png").convert_alpha()

    # --- Samurai4 ---
    images['samurai4_ATTACK1'] = pygame.image.load("assets/images/character/samurai4/Sprites/ATTACK1.png").convert_alpha()
    images['samurai4_ATTACK2'] = pygame.image.load("assets/images/character/samurai4/Sprites/ATTACK2.png").convert_alpha()
    images['samurai4_ATTACK3'] = pygame.image.load("assets/images/character/samurai4/Sprites/ATTACK3.png").convert_alpha()
    images['samurai4_DEATH'] = pygame.image.load("assets/images/character/samurai4/Sprites/DEATH.png").convert_alpha()
    images['samurai4_HURT'] = pygame.image.load("assets/images/character/samurai4/Sprites/HURT.png").convert_alpha()
    images['samurai4_IDLE'] = pygame.image.load("assets/images/character/samurai4/Sprites/IDLE.png").convert_alpha()
    images['samurai4_JUMP'] = pygame.image.load("assets/images/character/samurai4/Sprites/JUMP.png").convert_alpha()
    images['samurai4_RUN'] = pygame.image.load("assets/images/character/samurai4/Sprites/RUN.png").convert_alpha()
    images['samurai4_THROW'] = pygame.image.load("assets/images/character/samurai4/Sprites/THROW.png").convert_alpha()

    # --- Samurai5 ---
    images['samurai5_ATTACK1'] = pygame.image.load("assets/images/character/samurai5/Sprites/ATTACK1.png").convert_alpha()
    images['samurai5_ATTACK2'] = pygame.image.load("assets/images/character/samurai5/Sprites/ATTACK2.png").convert_alpha()
    images['samurai5_ATTACK3'] = pygame.image.load("assets/images/character/samurai5/Sprites/ATTACK3.png").convert_alpha()
    images['samurai5_DEATH'] = pygame.image.load("assets/images/character/samurai5/Sprites/DEATH.png").convert_alpha()
    images['samurai5_HURT'] = pygame.image.load("assets/images/character/samurai5/Sprites/HURT.png").convert_alpha()
    images['samurai5_IDLE'] = pygame.image.load("assets/images/character/samurai5/Sprites/IDLE.png").convert_alpha()
    images['samurai5_JUMP'] = pygame.image.load("assets/images/character/samurai5/Sprites/JUMP.png").convert_alpha()
    images['samurai5_RUN'] = pygame.image.load("assets/images/character/samurai5/Sprites/RUN.png").convert_alpha()

    # --- Samurai6 ---
    images['samurai6_ATTACK1'] = pygame.image.load("assets/images/character/samurai6/Sprites/ATTACK1.png").convert_alpha()
    images['samurai6_ATTACK2'] = pygame.image.load("assets/images/character/samurai6/Sprites/ATTACK2.png").convert_alpha()
    images['samurai6_ATTACK3'] = pygame.image.load("assets/images/character/samurai6/Sprites/ATTACK3.png").convert_alpha()
    images['samurai6_DEATH'] = pygame.image.load("assets/images/character/samurai6/Sprites/DEATH.png").convert_alpha()
    images['samurai6_HURT'] = pygame.image.load("assets/images/character/samurai6/Sprites/HURT.png").convert_alpha()
    images['samurai6_IDLE'] = pygame.image.load("assets/images/character/samurai6/Sprites/IDLE.png").convert_alpha()
    images['samurai6_JUMP'] = pygame.image.load("assets/images/character/samurai6/Sprites/JUMP.png").convert_alpha()
    images['samurai6_RUN'] = pygame.image.load("assets/images/character/samurai6/Sprites/RUN.png").convert_alpha()

    # --- Samurai7 Normal ---
    images['samurai7_ATTACK1'] = pygame.image.load("assets/images/character/samurai7/normal/ATTACK 1.png").convert_alpha()
    images['samurai7_ATTACK2'] = pygame.image.load("assets/images/character/samurai7/normal/ATTACK 2.png").convert_alpha()
    images['samurai7_ATTACK3'] = pygame.image.load("assets/images/character/samurai7/normal/ATTACK 3.png").convert_alpha()
    images['samurai7_DEATH'] = pygame.image.load("assets/images/character/samurai7/normal/DEATH.png").convert_alpha()
    images['samurai7_HURT'] = pygame.image.load("assets/images/character/samurai7/normal/HURT.png").convert_alpha()
    images['samurai7_IDLE'] = pygame.image.load("assets/images/character/samurai7/normal/IDLE.png").convert_alpha()
    images['samurai7_JUMP_ATTACK'] = pygame.image.load("assets/images/character/samurai7/normal/JUMP ATTACK.png").convert_alpha()
    images['samurai7_RUN'] = pygame.image.load("assets/images/character/samurai7/normal/RUN.png").convert_alpha()
    images['samurai7_SHOUT'] = pygame.image.load("assets/images/character/samurai7/normal/SHOUT.png").convert_alpha()

    # --- Samurai7 Flaming ---
    images['samurai7_attack1flaming'] = pygame.image.load("assets/images/character/samurai7/flaming/attack1flaming.png").convert_alpha()
    images['samurai7_attack2flaming'] = pygame.image.load("assets/images/character/samurai7/flaming/attack2flaming.png").convert_alpha()
    images['samurai7_attack3flaming'] = pygame.image.load("assets/images/character/samurai7/flaming/attack3flaming.png").convert_alpha()
    images['samurai7_DEATH_flaming'] = pygame.image.load("assets/images/character/samurai7/flaming/DEATH.png").convert_alpha()
    images['samurai7_hurtflaming'] = pygame.image.load("assets/images/character/samurai7/flaming/hurtflaming.png").convert_alpha()
    images['samurai7_idleflaming'] = pygame.image.load("assets/images/character/samurai7/flaming/idleflaming.png").convert_alpha()
    images['samurai7_jumpattackflamming'] = pygame.image.load("assets/images/character/samurai7/flaming/jumpattackflaming.png").convert_alpha()
    images['samurai7_runflaming'] = pygame.image.load("assets/images/character/samurai7/flaming/runflaming.png").convert_alpha()
    

    # --- Projectile ---
    images['shuriken'] = pygame.image.load("assets/images/projectile/shuriken.png").convert_alpha()

    # --- Background ---
    images['bg_map1'] = pygame.image.load("assets/images/background/map1night.png").convert_alpha()
    images['bg_map2'] = pygame.image.load("assets/images/background/map2.png").convert_alpha()
    images['mainmenu_bg'] = pygame.image.load("assets/images/background/mainmenu.png").convert_alpha()
    images['victory'] = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

    # --- Sounds ---
    pygame.mixer.music.load("assets/audio/music.mp3")
    sounds['sword_fx'] = pygame.mixer.Sound("assets/audio/sword.wav")
    sounds['shuriken_fx'] = pygame.mixer.Sound("assets/audio/shuriken.mp3")

def get_image(key):
    return images.get(key)

def get_sound(key):
    return sounds.get(key)
