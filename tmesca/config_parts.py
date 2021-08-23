class Generator:
  def __init__(self, config):
    self._config = config
  
  def type(self):
    if 'type' not in self._config:
      raise Exception('No type')
    return self._config['type']
  
  def link_length(self):
    if 'link_length' not in self._config:
      raise Exception('No link_length')
    return self._config['link_length']
  
  def restore_sessions(self):
    if 'restore_sessions' not in self._config:
      raise Exception('No restore_sessions')
    return self._config['restore_sessions']
  
  def save_sessions(self):
    if 'save_sessions' not in self._config:
      return True
    return self._config['save_sessions']

class Parser:
  def __init__(self, config):
    self._config = config

class Output:
  def __init__(self, config):
    self._config = config

class Session:
  pass