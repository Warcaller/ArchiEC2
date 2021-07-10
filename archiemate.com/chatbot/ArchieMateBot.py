#!/usr/bin/env python3
#coding=utf8

import json
import sys
from os import environ as env
from typing import List, Dict, Optional, Callable

from ArchieMate import Logger
import ArchieMate.Twitch.IRC as TwitchIRC
import ArchieMate.Poller as Poller
import ArchieMate.Commands as Commands
import ArchieMate.Variables as Variables

logger = Logger.get_logger(__name__)

def main() -> int:
  ARCHI_USER_ID: int = 147113965
  client_id: str = env.get("CLIENT_ID")
  client_secret: str = env.get("CLIENT_SECRET")
  oauth: str = env.get("OAUTH")
  channel: str = "archimond7450"
  bot_name: str = "archiemate"
  
  poller: Poller.Poller = Poller.Poller()
  
  twitch_ircs: Dict[int, TwitchIRC.IRC] = {
    channel: TwitchIRC.IRC(bot_name, channel, oauth, poller)
  }
  
  commands_json: dict = {}
  try:
    with open("json/commands.json", "r") as file:
      commands_json = json.load(file)
  except:
    logger.warning("Cannot parse commands.json")
  
  variables_json: dict = {}
  try:
    with open("json/variables.json", "r") as file:
      variables_json = json.load(file)
  except:
    logger.warning("Cannot parse variables.json")
  
  commands: Commands.Commands = Commands.Commands(commands_json)
  variables: Variables.Variables = Variables.Variables(variables_json)
  
  DEBUG: bool = env.get("DEBUG", "0") != "0"
  def send_debug_message_off(irc, message): pass
  def send_debug_message_on(irc, message):
    irc.send_message(message)
  send_debug_message: Callable = send_debug_message_on if DEBUG else send_debug_message_off
  
  logger.debug("START")
  
  done: bool = False
  while not done:
    # Timers - update from DB, write timer to IRC
    
    # Retrieve message from Twitch IRC
    for channel in twitch_ircs.keys():
      irc: TwitchIRC.IRC = twitch_ircs[channel]
      if msg := irc.recv():
        decoded_message = TwitchIRC.decode_message(msg)
        if isinstance(decoded_message, TwitchIRC.PrivMsg):
          priv_msg: TwitchIRC.PrivMsg = decoded_message
          send_debug_message(irc, f"/me received: '{priv_msg.message}'")
          
          channel_variables: Dict[str, str] = variables.get_variables(priv_msg.room_id)
          
          if detected_command := Commands.detect_command(priv_msg.message):
            chatters, command, arguments = detected_command
            if ("broadcaster" in priv_msg.badges or "mod" in priv_msg.badges) and command == "command":
              irc.send_message(f"@{priv_msg.display_name} {Commands.command_function(arguments, priv_msg.room_id, commands)}")
            elif priv_msg.user_id == ARCHI_USER_ID and command == "end":
              done = True
            elif priv_msg.user_id == ARCHI_USER_ID and command == "debug":
              if arguments == "on":
                send_debug_message = send_debug_message_on
              elif arguments == "off":
                send_debug_message = send_debug_message_off
              
            elif cmd := commands.find(priv_msg.room_id, command):
              try:
                irc.send_message(f"{cmd.function(chatters, priv_msg.display_name, arguments, channel_variables, None)}")
              except:
                logger.exception(f"Channel {priv_msg.room_id} command '!{command}' raised an exception!")
        
        elif isinstance(decoded_message, TwitchIRC.Ping):
          ping: TwitchIRC.Ping = decoded_message
          irc.send_pong(ping.server)
  
  for channel in twitch_ircs.keys():
    irc: TwitchIRC.IRC = twitch_ircs[channel]
    irc.send_message("ArchieMate is temporarily shutting down. HeyGuys")
  
  logger.debug("END")
  
  del twitch_ircs
  del poller
  
  commands_json: Dict[int, List[Dict[str, str]]] = commands.to_json()
  logger.debug(f"commands_json: {commands_json}")
  try:
    with open("json/commands.json", "w") as file:
      json.dump(commands_json, file)
  except:
    logger.exception("Cannot write to commands.json")
    pass
  
  variables_json: Dict[int, List[Dict[str, str]]] = variables.to_json()
  logger.debug(f"variables_json: {variables_json}")
  try:
    with open("json/variables.json", "w") as file:
      json.dump(variables_json, file)
  except:
    logger.exception("Cannot write to variables.json")
  
  return 0


if __name__ == '__main__':
  logger.debug("STARTED")
  code: int = main()
  logger.debug("TERMINATED")
  sys.exit(code)
