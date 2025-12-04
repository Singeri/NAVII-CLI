import json
import os

RC_FILE = os.path.join(os.path.expanduser("~"), ".navii_rc")

# iFlxy: not the first time cleaning up after someones chatgpt's bs... 
# Thanks iFlxy! My brain was scrambled after 4 hours of trying to debug this bs code after chatgpt completely rewrote all my FUCKING FUNCTIONS AND MADE IT RENDER COMPLETELY USELESS FOR NO REASON! I GAVE IT THE FUCKING COMMANDS TO ONLY TELL ME WHERE THE BUG IN MY ALIAS CODE IS NOT REWRITE ALL THE FUCKING COMMANDS WITHIN MY FUNCTIONS!!!!!!!!!!!!!!!!!!! 
# Oh and i rewrote the shell_alias a bit so it works better but now aliasing works
def check_alias(command):
    data = load_aliases()
    try:
        return data[command]
    except:
        return None

def load_aliases():
    if not os.path.exists(RC_FILE):
        with open(RC_FILE, 'w') as f:
            f.write("{}")
    try:
        with open(RC_FILE, "r") as f:
            return json.load(f)
            
    except Exception as e:
        print(f"Navii: Warning: Could not read alias file {RC_FILE}: {e}")

def save_alias(command, target):
    try:
        data = load_aliases()
        data[command] = target
        with open(RC_FILE, 'w') as f:
            f.write(json.dumps(data))
    except Exception as e:
        print(f"Navii: Warning: Could not write alias file {RC_FILE}: {e}")

def shell_alias(args):
    data = load_aliases()
    if len(args) == 0:
        if not data:
            print("No aliases defined.")
            return
        for name, target in data.items():
            print(f"{name}='{target}'")
        return
    
    if len(args) == 2:
        save_alias(args[0], args[1])
        return
    
    print("Navii: Invalid arguments! Usage: alias ALIAS COMMAND")