from utils.expands_vars import expand_vars_and_tilde
import os

def shell_cd(args):
    try:
        current_dir = os.getcwd()
    except OSError as e:
        print(f"Navii: cd: Error reading current directory: {e}")
        return 1
    
    target_path = None
    
    if not args:
        target_path = expand_vars_and_tilde("~")
        
    elif len(args) == 1:
        target_arg = args[0]
        
        if target_arg == '-':
            old_dir = os.environ.get('OLDPWD')
            if old_dir is None:
                print("Navii: cd: OLDPWD not set (first cd command hasn't been run yet)")
                return 1
            
            target_path = old_dir
            print(target_path)
            
        else:
            target_path = expand_vars_and_tilde(target_arg)
    else:
        print("Navii: cd: Too many arguments")
        return 1
    
    if target_path:
        try:
            os.chdir(target_path)
            
            os.environ['OLDPWD'] = current_dir
            return 0
        
        except FileNotFoundError:
            print(f"Navii: cd: Directory not found: {target_path}")
            return 1
        except NotADirectoryError:
            print(f"Navii: cd: Not a directory: {target_path}")
            return 1
        except PermissionError:
            print(f"Navii: cd: Permission denied: {target_path}")
            return 1
        except Exception as e:
            print(f"Navii: Error changing directory: {e}")
            return 1
    return 1
            