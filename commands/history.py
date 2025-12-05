import os

try:
    import readline
    USING_READLINE = True
except ImportError:
    try:
        from pyreadline3 import Readline
        readline = Readline()
        USING_READLINE = True
    except ImportError:
        readline = None
        USING_READLINE = False
        
def shell_history(args):
    if args:
        print("Navii: history: Command takes no arguments.")
        return 1
    
    if not USING_READLINE or not readline:
        print("Navii: History is not supported in this environment (readline/pyreadline3 not found).")
        return 1
    
    try:
        num_entries = readline.get_current_history_length()
        if num_entries == 0:
            print("History is empty")
            return 0
        
        print("/Command History/")
        for i in range(1, num_entries + 1):
            entry = readline.get_history_item(i)
            if entry:
                print(f" {i:4} {entry}")
        
        return 0
    
    except Exception as e:
        print(f"Navii: Error accessing history: {e}")
        return 1