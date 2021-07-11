import ArchieMate.Logger as Logger
from types import Callable, Dict, List, Optional, FunctionType, CodeType
from importlib import import_module
from enum import Enum
import regex as re

__empty_func__: Callable = lambda *args: None
__globals_commands__: Dict[str, any] = globals()

logger: Logger = Logger.get_logger(__name__)

__command_regex__ = re.compile(r"^(?P<chatters>(@\w+\s*,?\s*)*)!(?P<command>\w+)(?P<arguments>.*)$")
__command_function_regex__ = re.compile(r"^(?P<action>\w+)\s+!?(?P<command>\S+)(\s+(type=(?P<type>\w+)\s+))?(?P<response>.*)?$")

def detect_command(message: str) -> tuple[list[str], str, str]:
  if regex := __command_regex__.match(message):
    group_dict = regex.groupdict()
    
    chatters: str = ", ".join("".join(group_dict["chatters"].split()).split(",")) if "chatters" in group_dict else ""
    command: str = group_dict["command"].lower()
    arguments: str = group_dict["arguments"].strip() if "arguments" in group_dict else ""
    
    return chatters, command, arguments
  return ""

__globals_commands__["open"] = __empty_func__
__globals_commands__["close"] = __empty_func__
__globals_commands__["print"] = __empty_func__
__globals_commands__["exit"] = __empty_func__

__globals_commands__["sys"] = import_module("sys")
__globals_commands__["sys"].exit = __empty_func__
__globals_commands__["datetime"] = import_module("datetime")

__command_function_signature__: str = "def command(chatters, sender, arguments, variables, alert):"

class CommandType(Enum):
  StringType = 0
  SimpleType = 1
  CodeType = 2
  
def to_function_type(value: str) -> Optional[CommandType]:
  result: Optional[CommandType] = None
  if value == "string":
    result = CommandType.StringType
  elif value == "simple":
    result = CommandType.SimpleType
  elif value == "code":
    result = CommandType.CodeType
  logger.debug(f"to_function_type(value: '{value}') -> {result}")
  return result

def to_function_json_type(value: CommandType) -> str:
  result: str = ""
  if value == CommandType.StringType:
    result = "string"
  elif value == CommandType.SimpleType:
    result = "simple"
  elif value == CommandType.CodeType:
    result = "code"
  logger.debug(f"to_function_json_type(value: {value}) -> '{result}'")
  return result

class Function:
  def __init__(self, channel: int, name: str, type: CommandType, cooldown: int, code: str):
    logger.debug(f"Commands.Function.__init__(channel: {channel}, name: {name}, type: {type}, code: '{code}'")
    
    self.name: str = name
    self.type: CommandType = type
    self.cooldown: int = cooldown
    self.code: str = code
    self.channel: int = channel
    self.code_str: str = __command_function_signature__
    self.last_code_str: str = ""
    self.function: FunctionType = self.compile()
    
  def update(self, name: str, type: CommandType, code: str):
    logger.debug(f"Commands.Function.update(name: {name}, type: {type}, code: '{code}')")
    
    self.name = name
    self.type = type
    self.code = code
    backup_last_code_str = self.last_code_str
    self.last_code_str = self.code_str
    self.code_str = __command_function_signature__
    
    try:
      self.function = self.compile()
    except:
      logger.exception("Compiling failed!")
      self.last_code_str = backup_last_code_str
      raise
  
  def compile(self) -> FunctionType:
    logger.debug("Commands.Function.compile()")
    
    uniq_file: str = f"<string>.{self.channel}.{self.name}"
    logger.debug(f"uniq_file: {uniq_file}")
    
    if self.type == CommandType.StringType:
      self.code_str += f" return \"{self.code.strip()}\""
    elif self.type == CommandType.SimpleType:
      self.code_str += f" return str({self.code}).strip()"
    else:
      self.code_str += "\n"
      for line in self.code.strip().splitlines():
        self.code_str += f"\t{line.rstrip()}\n"
    
    logger.debug(f"Last code_str: '{self.last_code_str}'")
    logger.debug(f"New code_str:  '{self.code_str}'")
    
    if self.last_code_str != self.code_str:
      logger.debug("Code changed, compiling")
      command_code = compile(self.code_str, uniq_file, "exec")
      co_const: CodeType = None
      for c in command_code.co_consts:
        if isinstance(c, CodeType):
          co_const = c
          break
      return FunctionType(co_const, __globals_commands__)
    return self.function

class Commands:
  def __init__(self, json):
    logger.debug(f"Commands.__init__(json: {json})")
    
    self.commands: dict[int, list[Function]] = {}
    if not(json and isinstance(json, dict)):
      logger.debug("Parameter json is either empty or wrong. Skipping initialization.")
    else:
      for channel in json:
        logger.debug(f"Initializing commands for channel id {channel}")
        self.commands[int(channel)] = [Function(int(channel), command["name"], to_function_type(command["type"]), command["cooldown"], command["code"]) for command in json[channel]]
    logger.debug(f"Commands.__init__ done -> {self.__dict__}")
  
  def find(self, channel: int, command: str) -> Function:
    if channel not in self.commands:
      self.commands[channel] = []
    found: List[Function] = [cmd for cmd in self.commands.get(channel, []) if cmd.name == command]
    return found[0] if len(found) > 0 else None
  
  def delete(self, channel: int, command: str) -> bool:
    if self.find(channel, command) is not None:
      self.commands[channel] = [cmd for cmd in self.commands[channel] if cmd.name != command]
      return True
    return False
  
  def create(self, channel: int, command: str, type: CommandType, code: str) -> bool:
    if self.find(channel, command) is None:
      self.commands[channel].append(Function(channel, command, type, code))
      return True
    return False
  
  def update(self, channel: int, command: str, type: CommandType, code: str) -> bool:
    if cmd := self.find(channel, command):
      cmd.update(command, type, code)
      return True
    return False
  
  def to_json(self) -> dict[int, list[dict[str, str]]]:
    return {
      channel: [
        {
          "name": command.name,
          "type": to_function_json_type(command.type),
          "cooldown": command.cooldown,
          "code": command.code
        } for command in self.commands[channel]
      ] for channel in self.commands
    }

def command_function(arguments: str, channel: int, commands: Commands):
  if regex := __command_function_regex__.match(arguments):
    group_dict = regex.groupdict()
    if "action" in group_dict and "command" in group_dict and group_dict["action"] in ("add", "create", "edit", "update", "delete", "remove"):
      action: str = group_dict["action"]
      command: str = group_dict["command"]
      cmd_type: CommandType = to_function_type("string" if "type" not in group_dict or group_dict["type"] is None else group_dict["type"])
      response: str = "" if "response" not in group_dict or group_dict["response"] is None else group_dict["response"].strip()
      
      if action in ("delete", "remove"):
        try:
          if commands.delete(channel, command):
            return f"Command '!{command}' is successfully deleted."
        except:
          logger.exception(f"Raised exception when deleting channel {channel} command '!{command}'!")
        return f"Cannot delete command '!{command}'!"
      elif action in ("add", "create"):
        try:
          if commands.create(channel, command, cmd_type, response):
            return f"Command '!{command}' is sucessfully created."
          else:
            return f"Cannot create new command '!{command}' because it already exists!"
        except:
          logger.exception(f"Raised exception when creating channel {channel} command '!{command}'!")
        return f"Cannot create new command '!{command}' because the response is invalid!"
      elif action in ("edit", "update"):
        try:
          if commands.update(channel, command, cmd_type, response):
            return f"Command '!{command}' is successfully updated."
          else:
            return f"Cannot edit command '!{command}' because it doesn't exist!"
        except:
          logger.exception(f"Raised exception when updating channel {channel} command '!{command}'!")
        return f"Cannot create new command '!{command}' because the response is invalid!"
  return "Usage: !command add|create|edit|update|delete|remove [type=string|simple [response]]"
