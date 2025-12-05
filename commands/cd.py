from utils.expands_vars import expand_vars_and_tilde

import os

def shell_cd(args):
    if not args:
        try:
            os.chdir(expand_vars_and_tilde("~"))
            return 0
        except Exception as e:
            print(f"Navii: Didn't make it home. Error: {e}")
            return 1

    target = args[0]
    try:
        os.chdir(target)
        return 0
    except FileNotFoundError:
        print(f"Navii: Directory not found: {target}")
        return 1
    except Exception as e:
        print(f"Navii: Error changing directory: {e}")
        return 1