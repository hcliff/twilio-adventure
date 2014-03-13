import os
import main
import unittest
import tempfile

from adventure import Adventure as AdventureMachine

class AdventureTestCase(unittest.TestCase):

  def setUp(self):
    main.app.config['TESTING'] = True
    self.app = main.app.test_client()
    self.machine = AdventureMachine()
    self.machine.play() 

  def tearDown(self):
    pass

  def test_state_initial(self):
    self.assertEqual(self.machine.current_state.__name__, 'initial')

  def test_transition(self):
    output = self.machine.transition_to('craigslist')
    self.assertEqual(self.machine.current_state.__name__, 'craigslist')
    self.assertTrue(self.machine.visited(AdventureMachine.initial))

  def test_serial_killer(self):
    self.machine.transition_to('craigslist')
    self.machine.transition_to('initial')
    output = self.machine.transition_to('craigslist')
    idiot = "And now both of your kidneys are gone (seriously?)\na: Try again"
    self.assertEqual(output, [None, idiot])

  def test_reading_emails(self):
    self.machine.transition_to('emails')
    self.machine.transition_to('groveling_developer')
    self.machine.transition_to('emails')
    current_transitions = self.machine.current_state.transitions(self.machine)
    self.assertEqual(len(current_transitions.items()), 2)

  def test_mapping_letters(self):
    self.machine.transition_to('emails')
    self.machine.transition_to('b')
    self.machine.transition_to('a')
    self.machine.transition_to('b')
    self.assertEqual(self.machine.current_state.__name__, 'boss')

  def test_restart(self):
    self.machine.transition_to('emails')
    self.machine.transition_to('b')
    self.machine.transition_to('RESTART')
    self.assertEqual(self.machine.current_state.__name__, 'initial')

  def test_back(self):
    self.machine.transition_to('emails')
    self.machine.transition_to('b')
    self.machine.transition_to('BACK')
    self.assertEqual(self.machine.current_state.__name__, 'emails')

if __name__ == '__main__':
    unittest.main()