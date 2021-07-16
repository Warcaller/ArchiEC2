import ArchieMate.Logger as Logger
from typing import Dict, Optional, Any
import datetime

logger: Logger = Logger.get_logger(__name__)

class Channel:
  @staticmethod
  def create_new():
    logger.debug("Channel.create_new()")
    return Channel()
  
  def __init__(self, json: Optional[Dict[str, Any]] = None):
    logger.debug(f"Channel.__init__(json: {json})")
    self.points: int = int(json["points"]) if json is not None and "points" in json else 0
    self.mod: bool = json["mod"] if json is not None and "mod" in json else False
    self.commands: Dict[str, datetime.datetime] = {
      command: datetime.datetime.utcfromtimestamp(timestamp).replace(microsend=timestamp % (1000 * 1000))
      for command in json["commands"]
      if (timestamp := int(json["commands"][command]))
    } if json is not None and "commands" in json else {}
    logger.debug(f"Result: {self.__dict__}")
  
  def get_command(self, command: str) -> Dict[str, datetime.datetime]:
    logger.debug(f"Channel.get_command(command: {command})")
    if command not in self.commands:
      self.commands[command] = datetime.datetime.utcfromtimestamp(0)
    result = self.commands[command]
    logger.debug(f"self after: {self.__dict__}, result: {result}")
    return result

class User:
  @staticmethod
  def create_new(user: str, display_name: str, bot: bool):
    logger.debug(f"User.create_new(user: {user}, display_name: {display_name}, bot: {bot})")
    return User(user=user, display_name=display_name, bot=bot)
  
  def __init__(self, json: Optional[Dict[str, Any]] = None, **kwargs):
    logger.debug(f"User.__init__(json: {json}, **kwargs: {kwargs})")
    self.user: str = json["user"] if json is not None and "user" in json else kwargs["user"]
    self.display_name: str = json["display_name"] if json is not None and "display_name" in json else kwargs["display_name"]
    self.bot: bool = json["bot"] if json is not None and "bot" in json else kwargs["bot"]
    self.channels: Dict[int, Channel] = {
      channel: Channel(json["channels"][channel]) for channel in json["channels"]
    } if json is not None and "channels" in json else {}
    logger.debug(f"Result: {self.__dict__}")
  
  def get_channel(self, id: int) -> Channel:
    logger.debug(f"User.get_channel(id: {id})")
    if id not in self.channels:
      self.channels[id] = Channel.create_new()
    result = self.channels[id]
    logger.debug(f"self after: {self.__dict__}, result: {result}")
    return result

class Users:
  def __init__(self, json):
    logger.debug(f"Users.__init__(json: {json})")
    self.users: Dict[int, User] = {int(user): User(json[user]) for user in json}
    logger.debug(f"Result: {self.__dict__}")
  
  def to_json(self) -> Dict[int, Dict[str, any]]:
    logger.debug(f"Users.to_json()")
    result = {
      user: {
        "user": user_detail.user,
        "display_name": user_detail.display_name,
        "bot": user_detail.bot,
        "channels": {
          channel: {
            "points": channel_detail.points,
            "mod": channel_detail.mod,
            "commands": {
              command: command_detail.timestamp()
              for command in channel_detail.commands
              if (command_detail := channel_detail.commands[command])
            }
          } for channel in user_detail.channels
          if (channel_detail := user_detail.channels[channel])
        }
      } for user in self.users
      if (user_detail := self.users[user])
    }
    logger.debug("Result: {result}")
    return result
  
  def get_user(self, id: int, *, user: str, display_name: str) -> User:
    logger.debug(f"Users.get_user(id: {id}, user: {user}, display_name: {display_name})")
    if id not in self.users:
      self.users[id] = User.create_new(user, display_name, False)
    result = self.users[id]
    logger.debug(f"self after: {self.__dict__}, result: {result}")
    return result
  
  def get_user_by_name(self, user: str) -> User:
    logger.debug(f"Users.get_user_by_name(user: {user})")
    found = [one_user_detail for one_user in self.users if (one_user_detail := self.users[one_user]) and one_user_detail.user == user]
    result = found[0] if len(found) > 0 else None
    logger.debug(f"self after: {self.__dict__}, result: {result}")
    return result
