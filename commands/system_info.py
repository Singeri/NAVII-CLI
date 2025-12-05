import os
import getpass
import socket
import sys

def shell_hostname(args):
    if args:
        print("Navii: hostname: Command takes no arguments.")
        return 1
    
    try:
        print(socket.gethostname())
        return 0
    except Exception as e:
        print(f"Navii: hostname: Error retrieving hostname: {e}")
        return 1
    
def shell_id(args):
    if args:
        print("Navii: id: COmmand takes no arguments.")
        return 1
    
    try:
        uid = os.getuid()
        gid = os.getgid()
        username = getpass.getuser()
        
        print(f"uid={uid}({username}) gid={gid}")
        return 0
    
    except AttributeError:
        try:
            username = getpass.getuser()
            print(f"username={username}")
            print("Navii: id: Full UID/GID info unavailable on this system.")
            return 0
        except Exception as e:
            print(f"Navii: id: Error retrieving user identity: {e}")
            return 1
        except Exception as e:
            print(f"Navii: id: An unexpected error occurred: {e}")
            return 1