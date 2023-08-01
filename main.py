from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random






# Create a Perlin noise object with 4 octaves and a random seed
noise = PerlinNoise(octaves=4, seed=random.randint(1, 1000))

# Create the Ursina application
app = Ursina()

# Load textures from the 'assets' folder
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')

# Load punch sound
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)

# Block pick and selected block variables
block_pick = 1
selected_block = grass_texture

# Disable the FPS counter and hide the exit button
window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
    global block_pick

    # Check if left mouse or right mouse is held down
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    # Change block_pick based on number keys (1, 2, 3, 4)
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        # Call the superclass constructor
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=10,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # Play punch sound
                punch_sound.play()
                if block_pick == 1:
                    # Create a voxel with grass texture on left mouse click
                    voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2:
                    # Create a voxel with stone texture on left mouse click
                    voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 3:
                    # Create a voxel with brick texture on left mouse click
                    voxel = Voxel(position=self.position + mouse.normal, texture=brick_texture)
                if block_pick == 4:
                    # Create a voxel with dirt texture on left mouse click
                    voxel = Voxel(position=self.position + mouse.normal, texture=dirt_texture)
            if key == 'right mouse down':
                # Play punch sound
                punch_sound.play()
                # Destroy the voxel on right mouse click
                destroy(self)

class Sky(Entity):
    def __init__(self):
        # Create a sky entity with a sphere model and sky texture
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=500,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        # Create a hand entity with arm model and arm texture
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        # Move the hand to the active position
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        # Move the hand to the passive position
        self.position = Vec2(0.4, -0.6)

# Generate the Voxel terrain using Perlin noise
for z in range( 20):
    for x in range( 20):
        # Generate height using Perlin noise and adjust voxel position
        height = noise([x*0.01, z*0.01])
        height = math.floor(height * 15)
        voxel = Voxel(position=(x, height, z))

# Create the FirstPersonController, Sky, and Hand objects
player = FirstPersonController()
sky = Sky()
hand = Hand()

# Run the Ursina application
app.run()
