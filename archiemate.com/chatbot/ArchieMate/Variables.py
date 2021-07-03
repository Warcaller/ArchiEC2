class Variables:
  def __init__(self, json):
    self.variables = {int(channel): {variable: json[channel][variable] for variable in json} for channel in json}
  
  def get_variables(self, channel: int) -> dict[str, str]:
    if channel not in self.variables:
      self.variables[channel] = {}
    return self.variables[channel]
  
  def to_json(self) -> dict[int, dict[str, str]]:
    return self.variables
  