import regex as re
from typing import Optional, Dict, List
import datetime

import ArchieMate.Logger as Logger
import ArchieMate.Socket as Socket
import ArchieMate.Poller as Poller

logger = Logger.get_logger(__name__)


def parse_tags(tags: str) -> Dict[str,str]:
  if tags.endswith("@"): tags = tags[1:]
  return {} if tags is None or len(tags) == 0 else {one_tag[0]: one_tag[1] for tag in tags.split(";") if (one_tag := tag.split("="))}


def parse_badges(badges: str) -> Dict[str, int]:
  return {} if badges is None or len(badges) == 0 else {one_badge[0]: int(one_badge[1]) for badge in badges.split(",") if (one_badge := badge.split("/"))}


def escape_irc(display_name: str) -> str:
  return "" if display_name is None or len(display_name) == 0 else display_name.replace("\\s", " ").replace("\\\\", "\\").replace("\\:", ";")


def parse_emote_range(emote_range: str) -> List[tuple]:
  return [] if emote_range is None or len(emote_range) == 0 else [(int(one_range[0]), int(one_range[1]) - int(one_range[0])) for rng in emote_range.split(",") if (one_range := rng.split("-"))]


def parse_emotes(emotes: str) -> Dict[int, List[tuple]]:
  return {} if emotes is None or len(emotes) == 0 else {int(one_emote[0]): parse_emote_range(one_emote[1]) for emote in emotes.split("/") if (one_emote := emote.split(":"))}


def parse_emote_sets(emote_sets: str) -> List[int]:
  return [] if emote_sets is None or len(emote_sets) == 0 else [int(emote_set) for emote_set in emote_sets.split(",")]

class Message:
  def __init__(self):
    pass

  def __repr__(self):
    return f"{type(self).__name__}: {self.__dict__}"

  def __str__(self):
    return self.__repr__()

class Notice(Message):
  regex = re.compile(r":tmi\.twitch\.tv NOTICE \* :(?P<message>.*)")
  
  @staticmethod
  def match(message: str):
    return Notice.regex.match(message)
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Notice.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.message = group_dict["message"]
    
    logger.debug(f"Result: {self.__dict__}")

class Generic(Message):
  regex = re.compile(r":tmi\.twitch\.tv (?P<message_number>\d{3}) (?P<bot_user>\S+) :(?P<message>.*)")
  
  @staticmethod
  def match(message: str):
    regex = Generic.regex.match(message)
    logger.debug(f"Generic.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Generic.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.message_number = int(group_dict["message_number"])
    self.bot_user = group_dict["bot_user"]
    self.message = group_dict["message"]
    
    logger.debug(f"Result: {self.__dict__}")

class Ping(Message):
  regex = re.compile(r"^PING\s:(?P<server>.*)$")
  
  @staticmethod
  def match(message: str):
    regex = Ping.regex.match(message)
    logger.debug(f"Ping.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Ping.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.server = group_dict["server"]
    
    logger.debug(f"Result: {self.__dict__}")

class PrivMsg:
  __regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:(?P<user>\S+)!\S+@\S+\.tmi\.twitch\.tv\sPRIVMSG\s#(?P<channel>\S+)\s:(?P<message>.*)$")

  @staticmethod
  def match(message):
    regex = re.match(PrivMsg.__regex, message)
    logger.debug(f"PrivMsg.match(message: '{message}') -> {regex}")
    return regex

  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"PrivMsg.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags = parse_tags(group_dict["tags"])
    self.badge_info = int(tags.get("badge_info", "0"))
    self.badges = parse_badges(tags.get("badges", ""))
    self.bits = int(tags.get("bits", "0"))
    self.color = tags.get("color", "#FFFFFF")
    self.display_name = escape_irc(tags.get("display-name", ""))
    self.emotes = parse_emotes(tags.get("emotes", ""))
    self.message_id = tags.get("id", "")
    self.mod = tags.get("mod", "0") == "1"
    self.room_id = int(tags.get("room-id", "0"))
    self.subscriber = tags.get("subscriber", "0") == "1"
    tmi_sent_ts = int(tags.get("tmi-sent-ts", "0"))
    self.tmi_sent_timestamp = datetime.datetime.utcfromtimestamp(tmi_sent_ts // 1000).replace(microsecond=tmi_sent_ts % (1000 * 1000))
    self.turbo = tags.get("turbo", "0") == "1"
    self.user_id = int(tags.get("user-id", "0"))
    self.user_type = tags.get("user-type", "")
    self.user = group_dict["user"]
    self.channel = group_dict["channel"]
    self.message = group_dict["message"]
    logger.debug(f"Result: {self.__dict__}")

class UnknownMessage(Message):
  def __init__(self, message: str):
    logger.debug(f"UnknownMessage.__init__(message: '{message}')")
    Message.__init__(self)
    self.message = message
    logger.debug(f"Result: {self.__dict__}")

def decode_message(message: str) -> Message:
  for message_class in (PrivMsg, Notice, Generic, Ping):
    if regex := message_class.match(message):
      return message_class(regex)
  
  return UnknownMessage(message)

def send(channel: str, message: str) -> str:
  logger.debug(f"send(message: '{message}')")
  ret = f"PRIVMSG #{channel} :{message}"
  logger.debug(f"Result: '{ret}'")
  return ret

twitch_irc_address = "irc.chat.twitch.tv"
twitch_irc_port = 6667

class IRC:
  def __init__(self, bot_name: str, channel: str, oauth: str, poller: Poller.Poller):
    logger.debug(f"IRC.__init__(bot_name: '{bot_name}', channel: '{channel}', oauth: '{oauth}')")
    self.channel = channel
    self.socket = Socket.Socket(twitch_irc_address, twitch_irc_port, poller)
    self.socket.send(f"PASS oauth:{oauth}")
    self.socket.send(f"NICK {bot_name}")
    self.socket.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
    self.socket.send(f"JOIN #{channel}")
    
    if not(
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 1, "Welcome, GLHF!") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 2, "Your host is tmi.twitch.tv") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 3, "This server is rather new") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 4, "-") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 375, "-") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 372, "You are in a maze of twisty passages, all alike.") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 376, ">")
    ):
      logger.error("Authentication failed!")
      raise ValueError("Authentication failed!")
  
  def __del__(self):
    logger.debug("IRC.__del__()")
    self.flush()
  
  def send_message(self, message):
    logger.debug(f"IRC.send_message(message: '{message}')")
    self.socket.send(f"PRIVMSG #{self.channel} :{message}")
  
  def send_pong(self, server):
    logger.debug(f"IRC.send_pong(server: '{server}')")
    self.socket.send(f"PONG :{server}")
  
  def recv(self) -> str:
    ret = self.socket.recv()
    logger.debug(f"IRC.recv() -> '{ret}'")
    return ret
  
  def flush(self):
    logger.debug("IRC.flush()")
    self.socket.flush()

def checkGenericMessage(generic_message: Generic, message_number: int, message: str) -> bool:
  logger.debug(f"checkGenericMessage(generic_message: {generic_message}, message_number: {message_number}, message: '{message})")
  is_generic_message = isinstance(generic_message, Generic)
  is_right_generic_message = generic_message.message_number == message_number and generic_message.message == message
  ret = is_generic_message and is_right_generic_message
  logger.debug(f"is_generic_message: {is_generic_message}, is_right_generic_message: {is_right_generic_message} => Result: {ret}")
  return ret
