import pymel.core as pm
# the class that it is inside the class definition
# it is the class from where it is inheriting
# in this cas is the class object.

class Home(object):
    def __init__(self):
        self.inhabitants = 4
    @property
    def rig_node(self):
        rig_node_variable = pm.ls('rig_node')
        if not rig_node_variable:
            rig_node_variable = pm.group(name='rig_node', empty=True)
        else:
            rig_node_variable = rig_node_variable[0]

        return rig_node_variable

    def clean(self):
        print("I clean the house")


my_space_loc = pm.spaceLocator()
my_house = Home()
pm.parent(my_space_loc, my_house.rig_node)
my_second_space_loc = pm.spaceLocator()
my_second_space_loc.setParent(my_house.rig_node)



