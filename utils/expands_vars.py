import os

def expand_vars_and_tilde(command_string):
    if not command_string:
        return command_string

    result = []
    i = 0
    length = len(command_string)
    in_single = False
    in_double = False

    def expand_var_name(name):
        if os.name == 'nt':
            for key in os.environ:
                if key.lower() == name.lower():
                    return os.environ[key]
            return ""
        
        return os.environ.get(name, "")

    while i < length:
        ch = command_string[i]

        if ch == "\\":
            if i + 1 < length:
                result.append(command_string[i + 1])
                i += 2
                continue
            else:
                result.append("\\")
                i += 1
                continue

        if ch == "'" and not in_double:
            in_single = not in_single
            result.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            result.append(ch)
            i += 1
            continue

        if ch == "~" and not in_single and not in_double:
            prev_char = command_string[i - 1] if i > 0 else None
            if prev_char is None or prev_char.isspace():
                if i + 1 == length or command_string[i + 1] == "/" or command_string[i + 1].isspace():
                    normalized_home = os.path.expanduser("~")
                    normalized_home = os.path.normpath(normalized_home)
                    result.append(normalized_home)
                    i += 1
                    continue
            result.append("~")
            i += 1
            continue

        if ch == "$" and not in_single:
            if i + 1 >= length:
                result.append("$")
                i += 1
                continue

            if command_string[i + 1] == "{":
                j = i + 2
                var_name_chars = []
                while j < length and command_string[j] != "}":
                    var_name_chars.append(command_string[j])
                    j += 1
                if j < length and command_string[j] == "}":
                    var_name = "".join(var_name_chars)
                    result.append(expand_var_name(var_name))
                    i = j + 1
                    continue
                else:
                    result.append("${")
                    i += 2
                    continue
            else:
                j = i + 1
                var_name_chars = []
                while j < length and (command_string[j].isalnum() or command_string[j] == "_"):
                    var_name_chars.append(command_string[j])
                    j += 1
                if var_name_chars:
                    var_name = "".join(var_name_chars)
                    result.append(expand_var_name(var_name))
                    i = j
                    continue
                else:
                    result.append("$")
                    i += 1
                    continue

        result.append(ch)
        i += 1

    return "".join(result)
