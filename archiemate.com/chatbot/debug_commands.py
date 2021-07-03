from types import FunctionType, CodeType

from importlib import import_module

empty_func = lambda *args: None
globals_commands = globals()

globals_commands["open"] = empty_func
globals_commands["close"] = empty_func
globals_commands["print"] = empty_func
globals_commands["exit"] = empty_func

globals_commands["sys"] = import_module("sys")
globals_commands["sys"].exit = empty_func
globals_commands["datetime"] = import_module("datetime")

class Commands:
  def __init__(self, commands, channel):
    self.commands = {}
    for command in commands:
      if command["channel"] == channel:
        command_name = command["name"]
        command_code_str = "def command(arguments, variables):"
        command_uniq_file = f"<string>.{channel}.{command_name}"
        
        if command["type"] == "string":
          command_code_str += f" return \"{command['code'].strip()}\""
        elif command["type"] == "simple":
          command_code_str += f" return str({command['code']}).strip()"
        else:
          command_code_str += "\n"
          for line in command["code"].strip().splitlines():
            command_code_str += f"  {line}\n"
        print(command)
        print(command_code_str)
        print("====")
        
        command_code = compile(command_code_str, command_uniq_file, "exec")
        co_const: CodeType = None
        for c in command_code.co_consts:
          if isinstance(c, CodeType):
            co_const = c
            break
        command_func = FunctionType(co_const, globals_commands)
        self.commands[command_name] = command_func

commands = [
  {
    "channel": "archimond7450",
    "name": "constant",
    "type": "string",
    "code": "This is a test."
  },
  {
    "channel": "archimond7450",
    "name": "number",
    "type": "simple",
    "code": "222 + 444"
  },
  {
    "channel": "gnarve",
    "name": "number",
    "type": "simple",
    "code": "100 + 20 + 3"
  },
  {
    "channel": "archimond7450",
    "name": "now",
    "type": "code",
    "code":
      """
now = datetime.datetime.now()
f = open("test", "r")
close(f)
print(now)
exit(1)
sys.exit(0)
return f"{now:%H:%M:%S}"
      """
  },
  {
    "channel": "gnarve",
    "name": "exception",
    "type": "code",
    "code": "raise Error('This is a test')"
  }
]

commands_archimond7450 = Commands(commands, "archimond7450")
commands_gnarve = Commands(commands, "gnarve")
# careful with exceptions and web requests