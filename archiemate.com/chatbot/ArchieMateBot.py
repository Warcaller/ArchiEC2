#!/usr/bin/env python3
#coding=utf8

import json
import sys
from os import environ as env
from typing import List, Dict, Optional, Callable
import datetime

from ArchieMate import Logger
import ArchieMate.Twitch.IRC as TwitchIRC
import ArchieMate.Poller as Poller
import ArchieMate.Commands as Commands
import ArchieMate.Variables as Variables
import ArchieMate.Users as Users
import ArchieMate.Twitch.Helix as TwitchHelix
import ArchieMate.SocketServer as SocketServer
import ArchieMate.GoogleCloud as GoogleCloud

logger = Logger.get_logger(__name__)

def main() -> int:
  ARCHI_USER_ID: int = 147113965
  CLIENT_ID: str = env.get("CLIENT_ID")
  CLIENT_SECRET: str = env.get("CLIENT_SECRET")
  OAUTH: str = env.get("OAUTH")
  WEBSITE_SOCKET_AUTH_KEY = env.get("WEBSITE_SOCKET_AUTH_KEY")
  CHANNEL: str = "archimond7450"
  BOT_NAME: str = "archiemate"
  
  poller: Poller.Poller = Poller.Poller()
  
  twitch_ircs: Dict[str, TwitchIRC.IRC] = {
    CHANNEL: TwitchIRC.IRC(BOT_NAME, CHANNEL, OAUTH, poller)
  }
  
  socket_server: SocketServer.SocketServer = SocketServer.SocketServer(poller)
  
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
  
  users_json: dict = {}
  try:
    with open("json/users.json", "r") as file:
      users_json = json.load(file)
  except:
    logger.warning("Cannot parse users.json")
  
  commands: Commands.Commands = Commands.Commands(commands_json)
  variables: Variables.Variables = Variables.Variables(variables_json)
  users: Users.Users = Users.Users(users_json)
  
  active_users: Dict[int, set[Users.User]] = {}
  
  DEBUG: bool = env.get("DEBUG", "0") != "0"
  def send_debug_message_off(irc, message): pass
  def send_debug_message_on(irc, message):
    irc.send_message(message)
  send_debug_message: Callable = send_debug_message_on if DEBUG else send_debug_message_off
  
  logger.debug("START")
  
  last_timer: datetime.datetime = datetime.datetime.now()
  done: bool = False
  while not done:
    # Timers - update from DB, write timer to IRC
    now: datetime.datetime = datetime.datetime.now()
    if int((now - last_timer).total_seconds()) >= 60:
      last_timer = now
      for channel in active_users:
        for user in active_users[channel]:
          user.get_channel(channel).points += 1
      active_users = {}
    
    socket_server.check_sockets()
    for socket in socket_server.sockets:
      if msg := socket.socket.recv().strip():
        if not socket.state.get("authenticated", False): # Fresh socket - expect login
          if msg.startswith("AUTH OVERLAY "):
            socket.state["type"] = SocketServer.SocketType.Overlay
            if msg == f"AUTH OVERLAY {WEBSITE_SOCKET_AUTH_KEY}":
              socket.state["authenticated"] = True
              socket.socket.send("AUTH OK")
            else:
              socket.state["dead"] = True
              socket.socket.send("AUTH NOK")
          else:
            socket.state["dead"] = True
            socket.socket.send("AUTH NOK")
        elif msg == "END":
          socket.state["dead"] = True
    
    # Retrieve message from Twitch IRC
    for channel in twitch_ircs.keys():
      irc: TwitchIRC.IRC = twitch_ircs[channel]
      if msg := irc.recv():
        decoded_message = TwitchIRC.decode_message(msg)
        if isinstance(decoded_message, TwitchIRC.PrivMsg):
          priv_msg: TwitchIRC.PrivMsg = decoded_message
          send_debug_message(irc, f"/me received: '{priv_msg.message}'")
          
          channel_variables: Dict[str, str] = variables.get_variables(priv_msg.room_id)
          
          user: Users.User = users.get_user(priv_msg.user_id, user=priv_msg.user, display_name=priv_msg.display_name)
          user_channel: Users.Channel = user.get_channel(priv_msg.room_id)
          user_channel.mod = "mod" in priv_msg.badges
          if priv_msg.room_id not in active_users:
            active_users[priv_msg.room_id] = set()
          if user not in active_users[priv_msg.room_id]:
            active_users[priv_msg.room_id].add(users.get_user(priv_msg.user_id, user=priv_msg.user, display_name=priv_msg.display_name))
          
          if detected_command := Commands.detect_command(priv_msg.message):
            chatters, command, arguments = detected_command
            if ("broadcaster" in priv_msg.badges or "mod" in priv_msg.badges) and command == "command":
              irc.send_message(f"@{priv_msg.display_name} {Commands.command_function(arguments, priv_msg.room_id, commands)}")
            elif ("broadcaster" in priv_msg.badges or "mod" in priv_msg.badges) and command == "test_tts":
              text: str = GoogleCloud.user_text_to_ssml(priv_msg.display_name, priv_msg.message)
              audio: bytes = GoogleCloud.ssml_to_audio(text)
              for socket in socket_server.sockets:
                socket.socket.send(audio)
            elif priv_msg.user_id == ARCHI_USER_ID and command == "end":
              done = True
            elif priv_msg.user_id == ARCHI_USER_ID and command == "debug":
              if arguments == "on":
                send_debug_message = send_debug_message_on
              elif arguments == "off":
                send_debug_message = send_debug_message_off
            elif channel == CHANNEL and command == "fel":
              irc.send_message(f"@{priv_msg.display_name} you currently have {user_channel.points} fel.")
              
            elif cmd := commands.find(priv_msg.room_id, command):
              try:
                irc.send_message(f"{cmd.function(chatters, priv_msg.display_name, arguments, channel_variables, None)}")
              except:
                logger.exception(f"Channel {priv_msg.room_id} command '!{command}' raised an exception!")
        elif isinstance(decoded_message, TwitchIRC.Join):
          join: TwitchIRC.Join = decoded_message
          user_detail: Users.User = users.get_user_by_name(join.user)
          #if user_detail is not None:
          #  active_users[channel].add(users.get_user(user_detail.id))
        elif isinstance(decoded_message, TwitchIRC.Part):
          part: TwitchIRC.Part = decoded_message
          user_detail: Users.User = users.get_user_by_name(part.user)
          #if user_detail is not None and user_detail.id is not None:
          #  active_users[channel].remove(users.get_user(user_detail.id))
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
  
  users_json: Dict[int, List[Dict[str, str]]] = users.to_json()
  logger.debug(f"users_json: {users_json}")
  try:
    with open("json/users.json", "w") as file:
      json.dump(users_json, file)
  except:
    logger.exception("Cannot write to users.json")
  
  return 0


if __name__ == '__main__':
  logger.debug("STARTED")
  code: int = main()
  logger.debug("TERMINATED")
  sys.exit(code)

