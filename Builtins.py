from commands.cd import shell_cd
from commands.ls import shell_ls
from commands.mv import shell_mv
from commands.cp import shell_cp
from commands.echo import shell_echo
from commands.rm import shell_rm
from commands.mkdir import shell_mkdir
from commands.cat import shell_cat
from commands.touch import shell_touch
from commands.help_cmd import shell_help
from commands.sudo import shell_sudo
from commands.export_cmd import shell_export
from commands.unset_cmd import shell_unset
from commands.clear import shell_clear
from commands.pwd import shell_pwd
from utils.alias import shell_alias
from commands.unalias import shell_unalias
from commands.big_sister import big_sister_command
from commands.eye import run_eye
from commands.time import shell_time
from commands.history import shell_history
from commands.which import shell_which
from commands.sleep import shell_sleep
from commands.body_body_body import body_body_body
from commands.system_info import shell_hostname, shell_id

import sys

BUILTIN_COMMANDS = {
    "cat": shell_cat,
    "cd": shell_cd,
    "clear": shell_clear,
    "cp": shell_cp,
    "mv": shell_mv,
    "exit": sys.exit,
    "echo": shell_echo,
    "help": shell_help,
    "ls": shell_ls,
    "history": shell_history,
    "mkdir": shell_mkdir,
    "pwd": shell_pwd,
    "rm": shell_rm,
    "sudo": shell_sudo,
    "unset": shell_unset,
    "BODY": body_body_body,
    "which": shell_which,
    "sleep": shell_sleep,
    "hostname": shell_hostname,
    "id": shell_id,
    "export": shell_export,
    "touch": shell_touch,
    "time": shell_time,
    "alias": shell_alias,
    "unalias": shell_unalias,
    "big_sister": big_sister_command,
    "eye": run_eye
}