import os

def shell_which(args):
    if len(args) != 1:
        print("Navii: which: Usage: which <command_name>")
        return 1
    
    command_name = args[0]
    
    path_env = os.environ.get('PATH', '')
    if not path_env:
        print("Navii: PATH environment variable not set.")
        return 1
    
    path_dirs = path_env.split(os.pathsep)
    
    for directory in path_dirs:
        if not directory:
            continue
        
        full_path = os.path.join(directory, command_name)
        
        if os.name == 'nt':
            if os.path.exists(full_path):
                print(full_path)
                return 0
            
            for ext in ['.exe', '.bat', '.cmd', '.com']:
                path_with_ext = full_path + ext
                if os.path.exists(path_with_ext):
                    print(path_with_ext)
                    return 0
                
        else:
            if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                print(full_path)
                return 0
            
    print(f"Navii: which: {command_name} not found in PATH.")
    return 1