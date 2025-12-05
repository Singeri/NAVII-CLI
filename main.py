import os
import sys
import pathlib
import getpass
import shlex

try:
    # Linux/MacOS
    import readline
    USING_READLINE = True
except ImportError:
    try:
        # Windows
        from pyreadline3 import Readline
        readline = Readline()
        USING_READLINE = True
    except ImportError:
        readline = None
        USING_READLINE = False

from utils.expands_vars import expand_vars_and_tilde
from utils.redirect import execute_navii_redirect
from utils.pipe import execute_navii_pipe
from utils.alias import check_alias, save_alias, load_aliases
from commands.clear import shell_clear
from executor import execute_shell_command
from Builtins import BUILTIN_COMMANDS


HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".navii_history")
MAX_HISTORY_SIZE = 1000

def main():
    shell_clear(None) #NOTE: Argument is required yet not used, is it necessary?

    logo = """
  ____    ____  __ __   ____  ____ 
 |    \  /    ||  |  | |    ||    |
 |  _  ||  o  ||  |  |  |  |  |  | 
 |  |  ||     ||  |  |  |  |  |  | 
 |  |  ||  _  ||  :  |  |  |  |  | 
 |  |  ||  |  |\     /  |  |  |  | 
 |__|__||__|__| \ _ /  |____||____|
 """
    print(logo)

    if USING_READLINE and readline:
        try:
            readline.read_history_file(HISTORY_FILE)
        except FileNotFoundError:
            pass

    print("Welcome to Navii.")
    username = input("Enter your shell handle (e.g., miku): ").strip()
    if not username:
        try:
            username = getpass.getuser()
        except:
            username = "guest"

    print(f"Welcome home {username}\nType 'exit' to quit. Windows support was added! Type 'help' for command and function list.")


    while True:
        try:
            current_path = os.getcwd()
            display_path = "/" if current_path == "/" else os.path.basename(current_path)
            prompt = f"{username}@Navii:{display_path}$ "

            user_input = input(prompt)
            if not user_input.strip():
                continue

            expanded = expand_vars_and_tilde(user_input)
            parts = shlex.split(expanded)
            
            # Handle when expand_vars_and_tilde returns nothing
            if len(parts) == 0:
                continue
            command = parts[0]
            alsname = check_alias(command)
            if ">" in expanded or "<" in expanded:
                if alsname != None:
                    parts[0] = alsname
                execute_navii_redirect(" ".join(parts))
                continue

            if "|" in expanded:
                if alsname != None:
                    parts[0] = alsname
                    execute_navii_pipe(" ".join(parts))
                else:
                    execute_navii_pipe(expanded)
                continue

            if command in BUILTIN_COMMANDS:
                if alsname != None:
                    if alsname in BUILTIN_COMMANDS:
                        split_alsname = shlex.split(alsname)
                        BUILTIN_COMMANDS[split_alsname[0]](split_alsname[1:])
                    else:
                        execute_shell_command(alsname + " " + " ".join(parts[1:]))
                else:
                    BUILTIN_COMMANDS[command](parts[1:])
                continue
            
            if alsname != None:
                execute_shell_command(alsname + " " + " ".join(parts[1:]))
                continue

            execute_shell_command(expanded)

        except KeyboardInterrupt:
            print("\nInterrupted.")
        except EOFError:
            break
        
    if USING_READLINE and readline:
        try:
            readline.set_history_length(MAX_HISTORY_SIZE)
            readline.write_history_file(HISTORY_FILE)
        except:
            pass

if __name__ == "__main__":
    main()
