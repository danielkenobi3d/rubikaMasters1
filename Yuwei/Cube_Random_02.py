import random


def Create_Box_RandomHeight(cubes_per_side, distance=3):
    index_name = 0
    for each_x in range(cubes_per_side):
        for each_y in range(cubes_per_side):
            for each_z in range(cubes_per_side):
                index_name = index_name + 1
                random_height = random.randint(1,3)
                cube_transform, cube_creation = cmds.polyCube(name=f'Cube{index_name}')
                cmds.setAttr(f'{cube_transform}.translateX', distance * each_x)
                cmds.setAttr(f'{cube_transform}.translateZ', distance * each_z)
                cmds.setAttr(f'{cube_transform}.translateY', distance * each_y)
                cmds.setAttr(f'{cube_transform}.scaleY', random_height)

Create_Box_RandomHeight(5)
