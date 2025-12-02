# EnableNavii command is for the creator of this shell 'Singeri'


import os
import sys
import shlex
import subprocess
import shutil
import pathlib


def shell_cd(args):
    if not args:
        print("Usage: cd <directory>")
        return 1
    
    try:
        os.chdir(args[0])
        return 0
    except FileNotFoundError:
        print(f"Navii: Directory not found: {args[0]}")
        return 1
    except Exception as e:
        print(f"Navii: Error changing directory: {e}")
        return 1
    
def shell_mv(args):
    if len(args) != 2:
        print("Usage: mv <source> <destination>")
        return 1

    source, destination = args[0], args[1]

    try:
        shutil.move(source, destination)
        return 0
    except FileNotFoundError:
        print(f"Navii: mv: source '{source}' not found.")
        return 1
    except Exception as e:
        print(f"Navii: mv: error moving '{source}' to '{destination}': {e}")
        return 1

    
def shell_cp(args):
    if len(args) != 2:
        print("Usage: cp <source> <destination>")
        return 1
    
    source, destination = args[0], args[1]

    try:
        if os.path.isdir(source):
            print(f"Navii: cp: skipping directory '{source}': Recursive copy ('cp -r') is not implemented.")
            return 1
        else:
            shutil.copy(source, destination)
            return 0
    except FileNotFoundError:
        print(f"Navii: cp: source '{source}' not found.")
        return 1
    except IsADirectoryError:
        print(f"Navii: cp: target '{destination}' is a directory.")
        return 1
    except Exception as e:
        print(f"Navii: cp: error copying '{source}' to '{destination}': {e}")
        return 1

def shell_echo(args):
    print(" ".join(args))
    return 0

def shell_touch(args):
    if not args:
        print("Usage: touch <filename1> [filename2...]")
        return 1
    
    return_code = 0
    for filename in args:
        try:
            with open(filename, "a"):
                os.utime(filename, None) 
        except Exception as e:
            print(f"Navii: touch: cannot touch '{filename}': {e}")
            return_code = 1
    return return_code

def shell_cat(args):
    if not args:
        print("Usage: cat <filename1> [filename2...]")
        return 1
    
    return_code = 0
    for filename in args:
        try:
            with open(filename, 'r') as f:
                sys.stdout.write(f.read())
        except FileNotFoundError:
            print(f"Navii: cat: {filename}: No such file or directory")
            return_code = 1
        except IsADirectoryError:
            print(f"Navii: cat: {filename}: Is a directory")
            return_code = 1
        except Exception as e:
            print(f"Navii: cat: {filename}: Error reading file: {e}")
            return_code = 1
            
    return return_code 

def shell_ls(args):
    target_dir = args[0] if args else os.getcwd()

    if os.path.isfile(target_dir):
        print(target_dir)
        return 0
    
    try:
        items = os.listdir(target_dir)
        display_items = sorted({item for item in items if not item.startswith('.')})

        if not display_items:
            return 0
        
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        max_len = max(len(item) for item in display_items)
        column_width = max_len + 2
        num_columns = max(1, terminal_width // column_width)
        num_items = len(display_items)
        num_rows = (num_items + num_columns - 1) // num_columns

        for row in range(num_rows):
            line = []
            
            for col in range(num_columns):
                index = row + col * num_rows
                if index < num_items:
                    item = display_items[index]
                    line.append(item.ljust(column_width))

            print("".join(line))

        return 0
    
    except FileNotFoundError:
        print(f"Navii: ls: cannot access '{target_dir}': No such file or directory")
        return 1
    except NotADirectoryError:
        print(f"Navii: ls: cannot access '{target_dir}': Not a directory")
        return 1
    except PermissionError:
        print(f"Navii: ls: cannot access '{target_dir}': Permission denied")
        return 1
    except Exception as e:
        print(f"Navii: ls: an unexpected error occurred: {e}")
        return 1


def shell_clear(args):
    os.system('clear')
    return 0

def shell_pwd(args):
    print(os.getcwd())
    return 0

def shell_mkdir(args):
    if not args:
        print("Usage: mkdir <directory_name>")
        return 1
    

    return_code = 0
    for dirname in args:
        try:
            os.makedirs(dirname)
        except FileExistsError:
            print(f"Navii: mkdir: cannot create directory '{dirname}': File exists")
            return_code = 1
        except PermissionError:
            print(f"Navii: mkdir: failed to create directory '{dirname}': Permission denied")
            return_code = 1
        except OSError as e:
            print(f"Navii: mkdir: failed to create directory '{dirname}': OS Error: {e}")
            return_code = 1
        except Exception as e:
            print(f"Navii: mkdir: failed to create directory '{dirname}': Genetic Error: {e}")
            return_code = 1
    return return_code
    
def shell_rm(args):
    if not args:
        print("Usage: rm <file_or_directory>")
        return 1
    
    return_code = 0
    for target in args:
        try:
            if os.path.isdir(target):
                os.rmdir(target)
            else:

                os.remove(target)
        except FileNotFoundError:
            print(f"Navii: rm: cannot remove '{target}': no such file or directory")
            return_code = 1
        except NotADirectoryError:
            print(f"Navii: rm: cannot remove '{target}': Not a directory (try file removal)")
            return_code = 1
        except OSError as e:
            if "Directory not empty" in str(e):
                print(f"Navii: rm: cannot remove directory '{target}': Directory not empty (use 'rm -rf' equivalent for recursive removal)")
            else:
                print(f"Navii: rm: failed to remove '{target}': {e}")
            return_code = 1
        except Exception as e:
            print(f"Navii: rm: failed to remove '{target}': {e}")
            return_code = 1

def shell_help(args):
    script_dir = pathlib.Path(__file__).resolve().parent
    help_file_path = script_dir / "help_docs.txt"
    
    try:
        with open(help_file_path, 'r') as f:
            print(f.read())
        return 0
    except FileNotFoundError:
        print(f"Navii: help: Error: help file not found at {help_file_path}.")
        return 1
    except Exception as e:
        print(f"Navii: help: An error occurred while reading the help file: {e}")
        return 1


def execute_shell_command(full_command_string):
    try:
        command_parts = shlex.split(full_command_string)
        
        process = subprocess.run(
            command_parts,
            check=False,
            text=True
        )
        return process.returncode
    
    except FileNotFoundError:
        print(f"Navii: Command not found: {command_parts[0]}")
        return 127
    except Exception as e:
        print(f"Navii shell execution error: {e}")
        return 1


def execute_navii_redirect(user_input):
    if user_input.count('>') > 1 or user_input.count('<') > 1:
        print("Navii: Only single output (>) or input (<) redirection is supported.")
        return 1

    if '|' in user_input and ('>' in user_input or '<' in user_input):
         print("Navii: Cannot combine pipes and redirection in a single command yet.")
         return 1

    if user_input.split()[0] in ['cd', 'exit']:
        print(f"Navii: Command '{user_input.split()[0]}' is state-changing and cannot be redirected.")
        return 1

    try:
        process = subprocess.run(
            user_input,
            check=False,
            shell=True,
            executable='/bin/sh', 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        
        if process.stdout:
            sys.stdout.write(process.stdout)
        if process.stderr:
            sys.stderr.write(f"Redirection Error: {process.stderr}")

        return process.returncode

    except FileNotFoundError:
        print("Navii: System shell (/bin/sh) not found. Cannot execute redirected command.")
        return 127
    except subprocess.TimeoutExpired:
        print("Navii: Redirected command timed out.")
        return 1
    except Exception as e:
        print(f"Navii redirection execution error: {e}")
        return 1
    

def shell_sudo(args):
    if not args:
        print("Usage: sudo <commands> [args..]")
        return 1
    
    command_to_run = "sudo " + " ".join(shlex.quote(args) for args in args)
    try:
        process = subprocess.run(
            command_to_run,
            check=False,
            shell=True,
            executable='/bin/sh',
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )

        return process.returncode
    
    except FileNotFoundError:
        print("Navii: External 'sudo' program not found:")
        return 127
    except Exception as e:
        print(f"Navii sudo command execution error: {e}")
        return 1


def execute_navii_pipe(user_input):
    if user_input.count('|') != 1:
        print("Navii: Only single pipes are supported.")
        return 1

    if user_input.split()[0] in ['cd', 'exit'] or user_input.split('|', 1)[1].strip().split()[0] in ['cd', 'exit']:
        print("Navii: Cannot pipe state-changing commands ('cd', 'exit').")
        return 1

    try:
        process = subprocess.run(
            user_input,
            check=False,
            shell=True,
            executable='/bin/sh', 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        
        if process.stdout:
            sys.stdout.write(process.stdout)
        if process.stderr:
            sys.stderr.write(f"Pipe Error: {process.stderr}")

        return process.returncode

    except FileNotFoundError:
        print("Navii: System shell (/bin/sh) not found. Cannot execute piped command.")
        return 127
    except subprocess.TimeoutExpired:
        print("Navii: Pipe command timed out.")
        return 1
    except Exception as e:
        print(f"Navii piped command execution error: {e}")
        return 1


BUILTIN_COMMANDS = {
    'cat': shell_cat,
    'cd': shell_cd,
    'clear': shell_clear,
    'cp': shell_cp,
    'mv': shell_mv,
    'exit': sys.exit,
    'echo': shell_echo,
    'help': shell_help,
    'ls': shell_ls,
    'mkdir': shell_mkdir,
    'pwd': shell_pwd,
    'rm': shell_rm,
    'sudo': shell_sudo,
    'touch': shell_touch,
}


def main():
    os.system('clear')
    logo = """
 ____    ____  __ __  ____  ____ 
|    \  /    ||  |  ||    ||    |
|  _  ||  o  ||  |  | |  |  |  | 
|  |  ||     ||  |  | |  |  |  | 
|  |  ||  _  ||  :  | |  |  |  | 
|  |  ||  |  | \   /  |  |  |  | 
|__|__||__|__|  \_/  |____||____|
"""
    print(logo)
    
    print("Welcome to Navii.")
    
    username = input("Enter your shell handle (e.g., miku): ").strip()
    if not username:
        username = "guest"
    
    print(f"Welcome home {username}")
    print("Type 'exit' to quit. Pipes (|), Redirection (>, <), external functions and sudo are now supported. Type 'help' for command and function list.")
    
    while True:
        try:
            current_path = os.getcwd()
            if current_path == '/':
                display_path = '/'
            else:
                display_path = os.path.basename(current_path)

            prompt = f"{username}@Navii:{display_path}$ "
            user_input = input(prompt)

            if not user_input.strip():
                continue
            
            if '>' in user_input or '<' in user_input:
                execute_navii_redirect(user_input)
                continue

            if '|' in user_input:
                execute_navii_pipe(user_input)
                continue

            try:
                parts = shlex.split(user_input) 
            except ValueError:
                print("Navii: Invalid command quoting or syntax.")
                continue
            
            if not parts:
                continue

            command = parts[0]

            if command in BUILTIN_COMMANDS:
                if command == "exit":
                    print("Exiting Navii...")
                    BUILTIN_COMMANDS[command](parts[1:])
                elif command == "cd":
                    BUILTIN_COMMANDS[command](parts[1:])
                else:
                    BUILTIN_COMMANDS[command](parts[1:])
                        
            else:
                execute_shell_command(user_input)


        except KeyboardInterrupt:
            print("\nNavii: Operation interrupted.")
        except EOFError:
            print("\nExiting Navii...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
