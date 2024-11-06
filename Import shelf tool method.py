'''
/// The original that definitely works!
import sys
import importlib

import find_driver_letter as driver
importlib.reload(driver)

A_driver = driver.get_folder_letter("current_file_path")[:-1]
custom_path = f'{A_driver}\My_RIGGING/JmvsSCRIPTS/shelf_tools'
print(f"module imported from {custom_path}")
sys.path.append(custom_path)

#-----------------------------
import cLocs
importlib.reload(cLocs)   
cLocs.createLocator()
'''

import sys
import importlib

import find_driver_letter as driver
importlib.reload(driver)

A_driver = driver.get_folder_letter("Jmvs_current_file_path")
custom_path = f'{A_driver}JmvsShelfTools_Modelling' # My_RIGGING\JmvsSCRIPTS\JMVS_Working_Scripts\JMVS_Rigging_Tools\prefix_tools\Prefix_Ui_tools\ui_scripts
#another_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools/Prefix_Ui_tools/ui_scripts' 
print(f"module imported from {custom_path}")
sys.path.append(custom_path)
#-----------------------------
'''
import Jmvs_UIsetup_Removeprefix_tool
importlib.reload(Jmvs_UIsetup_Removeprefix_tool)
Jmvs_UIsetup_Removeprefix_tool.main()
'''
#-----------------------------
def get_module_path(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return "Module not found"
    
    return os.path.dirname(spec.origin)

# Example: Get the path of the 'os' module
module_name = 'JmvsM_add_prefix_tool_01_Tool'
module_path = get_module_path(module_name)
print(f"The path of the '{module_name}' module is: {module_path}")

# C:\Program Files\Autodesk\Maya2024\Python\lib\importlib
# D:\My_RIGGING/JmvsSCRIPTS/shelf_tools