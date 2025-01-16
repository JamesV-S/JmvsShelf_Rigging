
import os.path
import importlib

def getModule_path_tool(arg):
    module_name = arg
    def get_module_path(module_name):
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                return "Module not found. it's correct path hasn't been set yet!" 
        except ModuleNotFoundError as e:
            print(f"Module not found. it's correct path hasn't been set yet!")
        module_path = os.path.dirname(spec.origin)
        return module_path
        
    # Example: Get the path of the 'os' module   
    module_path = get_module_path(module_name)
    new_name = module_path.replace('/', '\\')
    print(f"The path of the '{module_name}' module is: {new_name}")
