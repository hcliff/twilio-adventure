import os

from flask import Flask, request, session
from twilio.rest import TwilioRestClient

from adventure import Adventure as AdventureMachine

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
client = TwilioRestClient("AC480eb2142836f87897a4e2461fe94a6b",
                          "6115137f8cb5a7805b3df4b671105476")

def twilio_output(to_number, output):
  client.messages.create(to=to_number, from_="+16463627058", body=output)

@app.route('/', methods=['GET', 'POST'])
def play_game():

  print 'picking up'
  print session.get('state')
  # pick up wherever we left off
  adventure = AdventureMachine(state=session.get('state'))
  from_number = request.form.get('From')
  choice = request.form.get('Body', '').lower()

  adventure.on_transition = lambda x,y: twilio_output(from_number, y)

  # As the user progresses save their state
  def save_state(state):
    print 'changing state'
    print state
    session['state'] = state
  adventure.on_state_change = save_state

  if not choice or not len(adventure._states):
    adventure.play()
  else:
    try:
      adventure.transition_to(choice)
    except:
      twilio_output(from_number, 'Not a valid choice')
  return ''

if __name__ == '__main__':
  app.run(debug=True)