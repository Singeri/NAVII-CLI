import datetime

def shell_time(args):
    if args:
        print("Navii: time: Command takes no arguments.")
        return 1
    
    current_time = datetime.datetime.now()
    
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Current system Time: {time_string}")
    return 0
    