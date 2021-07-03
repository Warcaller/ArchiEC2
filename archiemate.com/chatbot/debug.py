import sys
from os import environ as env
import datetime

client_id = env.get("CLIENT_ID")
client_secret = env.get("CLIENT_SECRET")
oauth = env.get("OAUTH")
channel = "archimond7450"
bot_nickname = "archiemate"

import twitch
import regex as re

import debug_commands as dc

command_regex = re.compile(r"^(?P<chatters>(@\w+\s*,?\s*)*)!(?P<command>\w+)(?P<arguments>.*)$")

command_function_regex = re.compile(r"^(?P<action>\w+)\s+!?(?P<command>\S+)(\s+(type=(?P<type>\w+)\s+))?(?P<response>.*)?$")

def command_function(arguments, variables) -> str:
    if regex := command_function_regex.match(arguments):
        group_dict = regex.groupdict()
        if "action" in group_dict and "command" in group_dict and group_dict["action"] in ("add", "create", "edit", "update", "delete", "remove"):
            action = group_dict["action"]
            command = group_dict["command"]
            cmd_type = "string" if "type" not in group_dict or group_dict["type"] is None else group_dict["type"]
            response = "" if "response" not in group_dict or group_dict["response"] is None else group_dict["response"].strip()
            
            if action in ("delete", "remove"):
                if command in dc.commands_archimond7450.commands:
                    dc.commands = [cmd for cmd in dc.commands if cmd["name"] != command]
                else:
                    return f"Error: cannot delete command '!{command}' because it doesn't exist."
            elif action in ("add", "create"):
                if command in dc.commands_archimond7450.commands:
                    return f"Error: cannot create new command '!{command}' because it already exists."
                else:
                    dc.commands.append({
                        "channel": "archimond7450",
                        "name": command,
                        "type": cmd_type,
                        "code": response
                    })
            elif action in ("edit", "update"):
                if command in dc.commands_archimond7450.commands:
                    dc.commands = [cmd for cmd in dc.commands if cmd["name"] != command]
                    dc.commands.append({
                        "channel": "archimond7450",
                        "name": command,
                        "type": cmd_type,
                        "code": response
                    })
                else:
                    return f"Error: cannot edit command '!{command}' because it doesn't exist."
            
            del dc.commands_archimond7450
            dc.commands_archimond7450 = dc.Commands(dc.commands, "archimond7450")
            
            if action in ("delete", "remove"):
                return f"Command '!{command}' is successfully deleted."
            elif action in ("add", "create"):
                return f"Command '!{command}' is successfully updated."
            elif action in ("edit", "update"):
                return f"Command '!{command}' is successfully created."
    
    return "Error: incorrect syntax. Usage: !command add|create|edit|update|delete|remove [type=string|simple] [response]"
    

def process_message(message: twitch.chat.Message) -> None:
    message.chat.send(f"/me received: {message.text}")
    if message.channel == channel and message.sender == channel:
        msg = message.text.strip()
        
        if regex := command_regex.match(msg):
            group_dict = regex.groupdict()
            chatters = ", ".join("".join(group_dict["chatters"].split()).split(",")) if "chatters" in group_dict else ""
            command = group_dict["command"].lower()
            arguments = group_dict["arguments"].strip() if "arguments" in group_dict else ""
            
            msg_sent = ""
            if command == "end":
                msg_sent = "/me See you later! HeyGuys"
                message.chat.irc.active = False
            elif command == "command":
                msg_sent = command_function(arguments, {})
            elif command in dc.commands_archimond7450.commands:
                msg_sent = f"{chatters} {dc.commands_archimond7450.commands[command](arguments, {})}"
            
            if len(msg_sent) > 0:
                message.chat.send(msg_sent)
        
        """contains_command = False
        msg_normalized = msg
        for command, func in dc.commands_archimond7450.commands.iter():
            if f"!{command}" in msg:
                contains_command = True
                while msg_normalized.startswith("@"):
                    space_pos = msg_normalized.find(" ")
                    if "!" in msg_normalized[1:space_pos]:
                        contains_command = False
                        break
                    msg_normalized = msg_normalized[space_pos:].strip()
                break
        
        if contains_command:
            msg = msg_normalized
        
        msg_args = ""
        if " " in msg:
            msg_args = msg[msg.find(" "):].strip()
            msg = msg[len(msg_args)].strip()
        
        print(msg)
        print(msg_args)
        
        msg_sent = ""
        if msg[0] == "!":
            msg = msg[1:]
            if msg == "end":
                msg_sent = "/me See you later! HeyGuys"
                message.chat.irc.active = False
            elif msg in dc.commands_archimond7450.commands:
                msg_sent = dc.commands_archimond7450.commands[msg](msg_args, {})
        
        if len(msg_sent) > 0:
            message.chat.send(msg_sent)"""

def main():
    bot_helix = twitch.Helix(client_id, client_secret, use_cache=True)
    
    chat = twitch.Chat(f"#{channel}", bot_nickname, f"oauth:{oauth}", helix=bot_helix)
    chat.send("/me test starting VoHiYo")
    chat.subscribe(process_message)

if __name__ == "__main__":
    sys.exit(main())
