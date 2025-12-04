import subprocess
import sys
import shlex

from utils.alias import check_alias

def execute_navii_redirect(user_input):
    if user_input.count(">") > 1 or user_input.count("<") > 1:
        print("Navii: Only single output (>) or input (<) redirection is supported.")
        return 1

    if "|" in user_input and (">" in user_input or "<" in user_input):
        print("Navii: Cannot combine pipes and redirection in a single command yet.")
        return 1

    tokens = shlex.split(user_input) if user_input.strip() else []
    alsname = check_alias(tokens[0])
    first_token = tokens[0] if tokens else ""

    if first_token in ["cd", "exit"]:
        print(f"Navii: Command '{first_token}' is state-changing and cannot be redirected.")
        return 1

    try:
        process = subprocess.run(
            user_input,
            check=False,
            shell=True,
            executable="/bin/sh",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
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