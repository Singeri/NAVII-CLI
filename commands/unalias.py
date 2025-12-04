import json
import os
from utils.alias import load_aliases

RC_FILE = os.path.join(os.path.expanduser("~"), ".navii_rc")

def shell_unalias(args):
    if len(args) != 1:
        print("Usage: unalias NAME")
        return
    
    name = args[0]
    data = load_aliases()

    if name not in data:
        print(f"unalias: '{name}' not found")
        return
    
    del data[name]

    try:
        with open(RC_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Navii: Warning: Could not write alias file: {e}")
        return
    
    print(f"Alias '{name}' removed.")