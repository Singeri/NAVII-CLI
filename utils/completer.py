import os
import glob
try:
    import readline
except ImportError:
    pass
from Builtins import BUILTIN_COMMANDS

def navii_completer(text, state):
    if state == 0:
        line = readline.get_line_buffer()
        start_index = readline.get_begidx()
        
        if start_index == 0:
            suggestions = get_command_suggestions(text)
        else:
            suggestions = get_path_suggestions(text)
        if not hasattr(navii_completer, 'matches'):
            navii_completer.matches = []
        navii_completer.matches = suggestions
        
    try:
        return navii_completer.matches[state]
    except IndexError:
        return None
    
def get_command_suggestions(text):
    matches = []
    
    for cmd in BUILTIN_COMMANDS:
        if cmd.startswith(text):
            matches.append(cmd + ' ')
            
    
    return matches


def get_path_suggestions(text):
    
    if text.startswith('~'):
        search_path = os.path.expanduser(text) + '*'
    else:
        search_path = text + '*'
    
    matches = []
    for p in glob.glob(search_path):
        if os.path.isdir(p):
            matches.append(p + os.sep)
        else:
            matches.append(p)
    return matches