import maya.cmds as cmds
from random import random

def create_grid(cubes_per_side, distanceX=3, distanceZ=3, scaleY=3):
    index_name = 0
    for each_x in range(cubes_per_side):
        index_name = index_name + 1
        for each_z in range(cubes_per_side):
                 cube_transform, cube_creation = cmds.polyCube(name=f'Cube{index_name}')
                 cmds.setAttr(f'{cube_transform}.translateX', distanceX*each_x)
                 cmds.setAttr(f'{cube_transform}.translateZ', distanceZ*each_z)
                 cmds.setAttr(f'{cube_transform}.scaleY', int(random()*10+1))

create_grid(int(random()*10))
