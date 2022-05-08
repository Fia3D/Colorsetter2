bl_info = {
    'name': 'Colorsetter BETA',
    'category': 'All',
    'version': (0, 1, 2),
    'blender': (2, 90, 0)
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
