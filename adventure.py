import state

class Adventure(state.Machine):
  
  def play(self):
    self.transition_to('initial')

  def back_enter(adventure):
    # Not the current state, but the one prior to that
    previous_state = adventure._states[-2]
    # Transition to this prior state
    adventure.transition_to(previous_state)
    # And stop transitioning to 'BACK'
    raise state.NoTransition

  BACK = state.State(title="Try again",
                     enter=back_enter)

  def restart_enter(adventure):
    # Clear prior events
    adventure._states = []
    # Go back to the beginning
    adventure.transition_to('initial')
    # And stop transitioning to 'RESTART'
    raise state.NoTransition

  RESTART = state.State(title="Restart",
                        enter=restart_enter)

  enter_message = "It's another day at twillio's HR department and you're looking to kill some time"
  initial = state.State(title='Initial state',
                        transitions=['craigslist', 'emails'],
                        enter_message=enter_message)

  def craigslist_enter_message(adventure):
    craigslist_serial_killer = adventure.visited(adventure.craigslist)
    message = "You wake up in an ice bath missing a kidney."
    if craigslist_serial_killer:
      message = "And now both of your kidneys are gone (seriously?)"
    return message

  craigslist = state.State(title='Browse Craigslist',
                           transitions=['BACK'],
                           enter_message=craigslist_enter_message)

  def emails_transitions(adventure):
    transitions = state.Transitions()
    if not adventure.visited(adventure.deposed_king):
      transitions.append(adventure.deposed_king)
    if not adventure.visited(adventure.groveling_developer):
      transitions.append(adventure.groveling_developer)
    if not adventure.visited(adventure.boss):
      transitions.append(adventure.boss)
    return transitions

  def emails_enter_message(adventure):
    emails = len(adventure.emails.transitions(adventure))
    message = "You have %s emails:" % emails
    return message

  emails = state.State(title='Check your email',
                       transitions=emails_transitions,
                       enter_message=emails_enter_message)
  ignore_email_transition = state.Transition(state=emails, title='Ignore it')

  enter_message = "It's an email from your long lost recently-deposed uncle who's have some cash flow trouble"
  deposed_king = state.State(title="FROM: deposedking@hotmail.com",
                             transitions=['wire_fraud', 'question_king'],
                             enter_message=enter_message)


  wire_fraud = state.State(title="Wire him some money",
                           transitions=[
                            state.Transition(state=emails, 
                                             title='Pat yourself on the back'),
                            state.Transition(state=emails, 
                                             title='Instant remorse')
                           ],
                           enter_message="You wire your childs college savings")

  enter_message = "Something about timeshares and penny stocks. sounds legit."
  question_king = state.State(title="Question him some more",
                              transitions = [
                                state.Transition(state=wire_fraud, 
                                                 title="Wire him some money"),
                                ignore_email_transition,
                              ],
                              enter_message=enter_message)

  enter_message = "It's a groveling email looking for a job"
  groveling_developer = state.State(title="FROM: h.a.clifford@gmail.com",
                                    transitions= [
                                      ignore_email_transition,
                                      ignore_email_transition,
                                      ignore_email_transition
                                    ],
                                    enter_message=enter_message)

  enter_message = "Looks like your TPS reports were filled out incorrectly"
  boss = state.State(title="FROM: yourboss@twillio.com",
                     transitions=['seppuku', 'tps'],
                     enter_message=enter_message)

  seppuku = state.State(title="Seppuku",
                        transitions=['BACK'],
                        enter_message="An honourable death")

  enter_message = "After 32 straight hours at the office you have a minor breakdown"
  tps = state.State(title="Work the weekend",
                    transitions=['insanity','caffinated','exploitation'],
                    enter_message=enter_message)

  enter_message = "You're certified insane. You start a successful visual basic consultancy. You win!"
  insanity = state.State(title = "Where did these tangerines come from?",
                         transitions=['RESTART'],
                         enter_message=enter_message)

  enter_message = "You get everything done, but your stomach's playing up from all those energy drinks"
  caffinated = state.State(title = "Load up on energy drinks and power through",
                           transitions=['stall', 'urinal'],
                           enter_message=enter_message)

  exploitation = state.State(title = "Hire illegal immigrants to do the work for you",
                             transitions=['mcdonalds', 'kfc'],
                             enter_message="It's the american way!")

  enter_message = "That bigmac's not sitting well with your stomach"
  mcdonalds = state.State(title = "Relax and enjoy several mcdonalds",
                          transitions=['stall', 'urinal'],
                          enter_message=enter_message)
                          
  enter_message = "That chicken's not sitting well with your stomach"
  kfc = state.State(title="Relax and ejoy a KFC family bucket",
                    transitions=['stall', 'urinal'],
                    enter_message=enter_message)

  enter_message = "While minding your business you overhear Jeff Lawsons secret meeting to sell twillio to verizon"
  stall = state.State(title = "Bathroom stall",
                      transitions=['verizon', 'shady_dealings'],
                      enter_message=enter_message)

  verizon = state.State(title = "Verizon? seriously?",
                        transitions=['hide'],
                        enter_message="Yup")

  shady_dealings = state.State(title="Why is Jeff Lawson having shady phone calls in the bathroom?",
                               transitions=['hide'],
                               enter_message="Beats me. You work there; you ask him.")

  enter_message = "How do you stop Jeff realizing you are also in the bathroom?"
  hide = state.State(title = "Uh.. ok?",
                     transitions=['trex', 'die_horribly'],
                     enter_message=enter_message)

  enter_message = "Much like the t-rex Jeff's vision is motion based, good job."
  trex = state.State(title = "Sit perfectly still and make no sound",
                     transitions=['victory'],
                     enter_message=enter_message)

  def victory_enter_message(adventure):
    kidneys_missing = adventure.visited(adventure.craigslist)
    scammed = bool(adventure.visited(adventure.wire_fraud))
    disemboweled = bool(adventure.visited(adventure.seppuku))
    message = "When Jeff's gone you place a call to the board and his evil plans are thwarted, good job!\n"
    if(kidneys_missing or scammed or disemboweled):
      message += "It's a bit of a hollow victory though "
      if(disemboweled and scammed):
        message += "as you gave your money to scammers and disemboweled yourself"
      elif disemboweled:
        message += "as you disemboweled yourself"
      elif(kidneys_missing and scammed):
        message += "as scammers took your money and a kidney or two"
      else:
        message += "as you should probably see a docter about that missing kidney"
    else:
      message += "You are promoted to 'Assistant to the regional manager'"
    return message

  victory = state.State(title="Thanks! I watched a lot of jurrasic park growing up",
                        transitions=['RESTART'],
                        enter_message=victory_enter_message)

  die_horribly = state.State(title = "Nothing. What's he going to do?",
                             transitions=['BACK'],
                             enter_message="You are caught and eaten.")

  enter_message="You animal. You are caught and flayed by the maintance team."
  urinal = state.State(title = "Urinal",
                       transitions=['BACK'],
                       enter_message=enter_message)