
import os.path
import importlib

def getModule_path_tool(arg):
    module_name = arg
    def get_module_path(module_name):
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return "Module not found. it's correct path hasn't been set yet!" 
        
        return os.path.dirname(spec.origin)
        
    # Example: Get the path of the 'os' module   
    module_path = get_module_path(module_name)
    print(f"The path of the '{module_name}' module is: {module_path}")

#getModule_path_tool("OPM")
