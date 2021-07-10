from typing import Dict

class Variables:
  def __init__(self, json):
    self.variables: Dict[int, str] = {int(channel): {variable: json[channel][variable] for variable in json} for channel in json}
  
  def get_variables(self, channel: int) -> Dict[str, str]:
    if channel not in self.variables:
      self.variables[channel] = {}
    return self.variables[channel]
  
  def to_json(self) -> dict[int, Dict[str, str]]:
    return self.variables
  