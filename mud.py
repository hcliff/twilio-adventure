import sys

from adventure import Adventure as AdventureMachine

if __name__ == '__main__':
  adventure = AdventureMachine()

  def print_output(from_result, to_result):
    print to_result
    input = raw_input("choose: ")
    # Wrapping around incorrect choices
    try:
      adventure.transition_to(input)
    except:
      print_output(None, "Not a valid choice")

  adventure.on_transition = print_output
  adventure.play()