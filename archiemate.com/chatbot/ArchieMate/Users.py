import ArchieMate.Logger as Logger
from types import Dict, List, Optional, Any
import datetime

logger: Logger = Logger.get_logger(__name__)

class Channel:
  @staticmethod
  def create_new(id: int):
    return Channel(id=id)
  
  def __init__(self, json: Optional[Dict[str, Any]], **kwargs):
    self.points: int = int(json["points"]) if json is not None and "points" in json else 0
    self.mod: bool = json["mod"] if json is not None and "mod" in json else False
    self.__commands: Dict[str, datetime.datetime] = {
      command: datetime.datetime.utcfromtimestamp(timestamp).replace(microsend=timestamp % (1000 * 1000))
      for command in json["commands"]
      if (timestamp := int(json["commands"][command]))
    } if json is not None and "commands" in json else {}
  
  def get_command(self, command: str) -> Dict[str, datetime.datetime]:
    if command not in self.__commands:
      self.__commands[command] = datetime.datetime.utcfromtimestamp(0)
    return self.__commands[command]

class User:
  @staticmethod
  def create_new(id: int, user: str, display_name: str, bot: bool):
    return User(id, user=user, display_name=display_name, bot=bot)
  
  def __init__(self, json: Optional[Dict[str, Any]], **kwargs):
    self.user: str = json["user"] if "user" in json else kwargs["user"]
    self.display_name: str = json["display_name"] if json is not None and "display_name" in json else kwargs["display_name"]
    self.bot: str = json["bot"] if "bot" in json else kwargs["bot"]
    self.__channels: Dict[int, Channel] = {
      channel: Channel(json["channels"][channel]) for channel in json["channels"]
    } if json is not None and "channels" in json else {}
  
  def get_channel(self, id: int) -> Channel:
    if id not in self.__channels:
      self.__channels[id] = Channel.create_new(id)
    return self.__channels[id]

class Users:
  def __init__(self, json):
    self.users: Dict[int, User] = {int(user): User(json[user]) for user in json}
  
  def to_json(self) -> Dict[int, Dict[str, any]]:
    return {
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
              for command in channel_detail.__commands
              if (command_detail := channel_detail.__commands[command])
            }
          } for channel in user_detail.__channels
          if (channel_detail := user_detail.__channels[channel])
        }
      } for user in self.users
      if (user_detail := self.users[user])
    }
