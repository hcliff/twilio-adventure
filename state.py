from string import lowercase
from collections import OrderedDict

class StateClass(object):

  def __init__(self, title=None, transitions=None, enter_message=None, enter=None):
    self.title = title
    self.transitions = transitions
    self.enter_message = enter_message
    self.enter_fn = enter

  def leave(self):
    pass
  def enter(self, machine):
    if self.enter_fn:
      return self.enter_fn(machine)
    enter_message = self.enter_message
    if callable(enter_message):
      enter_message = enter_message(machine)
    transitions = self.transitions
    if callable(transitions):
      transitions = transitions(machine)
    return "%s\n%s" % (enter_message, transitions)

  @property
  def __name__(self):
    if self.name:
      return self.name
    return super(StateClass, self).__name()

class MachineOptions(object):
  states = {}

class MachineMeta(type):

  # When a class is constructed generate a list of it's states
  def __new__(cls, name, bases, attrs):
    new_class = super(MachineMeta, cls).__new__(cls, name, bases, attrs)
    module = attrs.pop('__module__')
    # Attach an options class to hold meta information
    new_class._meta = MachineOptions()
    
    # Loop through all the attributes and add states to the meta
    for obj_name, obj in attrs.items():
      is_state = isinstance(obj, StateClass)
      if is_state:
        new_class._meta.states[obj_name] = obj

    return new_class

class Machine(object):
  __metaclass__ = MachineMeta
  # Holds an array of every state we've been to
  _states = []
  on_transition = lambda x, y, z:x
  on_state_change = lambda x, y: x

  def __init__(self, state=None):
    # Resume mid game
    self._states = []
    if state:
      self._states = state

    # The meta class gives us a list of all our states
    for name, state in self._meta.states.iteritems():
      transitions = state.transitions
      def mapper(x):
        if isinstance(x, Transition):
          return x
        return Transition(state=getattr(self, x))
      # If needed, construct a `Tranisitions` object from an array
      if (transitions and 
          not callable(transitions) and 
          not isinstance(transitions, Transitions)):
        transitions = Transitions(*map(mapper, transitions))

      setattr(state, 'name', name)
      setattr(state, 'transitions', transitions)
      setattr(self, name, state)

  def transition_to(self, state):
    from_result = to_result = None
    
    # If currently in a state
    # 1) we can do relative tranisitions (e.g a,b,c)
    # 2) we will need to leave this state
    if self.current_state:
      transitions = self.current_state.transitions
      if callable(transitions):
        transitions = transitions(self)
      if transitions.has_key(state):
        state = transitions.get(state)['state'].__name__
      from_result = self.current_state.leave()

    # Assert we're in a real class
    to_state_class = getattr(self, state, None)
    assert to_state_class

    try:
      to_result = to_state_class.enter(self)
      self._states.append(to_state_class.__name__)
      # Fire listening events
      self.on_transition(from_result, to_result)
      self.on_state_change(self._states)
    # Allow transitions to block beind transitioned to
    except NoTransition:
      pass

    return [from_result, to_result]

  @property
  def current_state(self):
    if len(self._states):
      return getattr(self, self._states[-1])
    return None

  def visited(self, x):
    return self._states.count(getattr(x, '__name__', x))

  def transitions_factory(self, *transitions):
    def mapper(x):
      if isinstance(x, basestring):
        return getattr(self, transition)
      return x
    return map(mapper, transitions)

def State(*args, **kwargs):
  return StateClass(**kwargs)

class Transitions(OrderedDict): 

  def __init__(self, *args, **kwargs):
    self.lowercase = iter(lowercase)    
    super(Transitions, self).__init__()
    for value in args:
      self.append(value)

  def __str__(self):
    # pretty print all our options
    return "\n".join(map(lambda x: "%s: %s" % x, self.iteritems()))

  def append(self, value):
    def transition_factory(x):
      if isinstance(x, Transition):
        return x
      return Transition(state=x)
    # Take in a value and auto generate a key based on the alphabet
    self[self.lowercase.next()] = transition_factory(value)
    return self

class Transition(dict):

  def __str__(self):
    return str(self['title'])

  def __init__(self, *args, **kwargs):
    # If given a title explicity use it, otherwise grab the states default
    kwargs['title'] = kwargs.get('title', getattr(kwargs.get('state'), 'title'))
    return super(Transition, self).__init__(*args, **kwargs)

class NoTransition(Exception):
  pass