bl_info = {
    'name': 'Colorsetter2',
    'category': 'All',
    'version': (1, 0, 0),
    'blender': (3, 1, 0)
}

from . import materialProperties
from . import materialPanel
from . import materialOperators
 
 
def register():
    materialProperties.register()
    materialPanel.register()
    materialOperators.register()
 
 
def unregister():
    materialProperties.unregister()
    materialPanel.unregister()
    materialOperators.unregister()
 
 
if __name__ == "__main__":
    register()
