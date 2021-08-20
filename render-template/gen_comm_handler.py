import os
import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)
from render_template import *

cmd_list = [
    [ "GENERAL_CMD_SET            ", "REBOOT_REQUEST_CMD                "],
    [ "GENERAL_CMD_SET            ", "VERSION_REQUEST_CMD               "],
    [ "GENERAL_CMD_SET            ", "VERSION_REPLY_CMD                 "],
    [ "GENERAL_CMD_SET            ", "ERASE_APP_REQUEST_CMD             "],
]

args = {
    "cmd_list": list(map(lambda x: [x[0].strip(), x[1].strip()], cmd_list))
}

render_template("comm_handler_table.c.jinja2", "comm_handler_table.c", args)
