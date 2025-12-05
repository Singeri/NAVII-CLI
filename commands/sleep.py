import time
import sys

def shell_sleep(args):
    if len(args) != 1:
        print("Navii: sleep: Usage: sleep <seconds>")
        return 1
    
    try:
        seconds = float(args[0])
        
        if seconds < 0:
            print("Navii: sleep: cannot sleep for negative time")
            return 1
        
        if seconds == 0:
            return 0
        
        time.sleep(seconds)
        return 0
    
    except ValueError:
        print(f"Navii: sleep: invalid time interval '{args[0]}'")
        return 1
    except KeyboardInterrupt:
        print("\nNavii: sleep: interrupted")
        return 1