
import json


# ------------------------- Non-speaking Part ----------------------------------

def current_time():
    time = datetime.datetime.now().strftime("%A %d %B %Y %I %M %p")
    time = time.split()
    print(time)
    if int(time[4]) < 12 and int(time[4]) > 7 and time[6] == "AM":
        return "Morning"
    elif (int(time[4]) < 4 and time[6] == "PM") or (int(time[4]) == 12 and time[6] == "PM"):
        return "Afternoon"
    elif int(time[4]) < 8 and int(time[4]) > 3 and time[6] == "PM":
        return "Evening"
send_url = 'http://ipinfo.io/json'
r = requests.get(send_url)
j = json.loads(r.text)
curr_loca = str(j["city"])
print("Will you stay in " + curr_loca + " for the whole day or go somewhere else?")
curr_time = current_time()

'''

#

# ----------------------- Just for testing use ---------------------------------
'''
curr_weather = "rainy"
curr_clothes = "thick coat"

'''

fu_weather = "warmer"
fu_clothes = "thinner coat"


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_Start_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Start"
    speech_output = "Will you stay in Albany County for the whole day or go somewhere else?"
    reprompt_text = "I don't know if you heard me" + speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_StayHere_response():
    session_attributes = {}
    card_title = "StayHere"
    speech_output = "It's cold weather with little to no winds in Albany and you can wear long sleeve shirt, coat, pants, and sneakers. " 
    reprompt_text = "say it again please"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_GoOtherPla_response(fu_loca):
    session_attributes = {}
    card_title = "GoOther"
    speech_output = "It's cold weather with little to no winds in Albany and you may wear long sleeve shirt, coat, pants, and sneakers. Considering that you will go to " + fu_loca + " where it will be " + fu_weather + ", so you should think about wearing " + fu_clothes + " there."
    reprompt_text = "say it again please"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hi, how can I help you?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, How can I help you?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for Using our service. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    # Dispatch to your skill's intent handlers
    if intent_name == "Start":
        return get_Start_response()
    elif intent_name == "StayHere":
        return get_StayHere_response()
    elif intent_name == "GoOther":
        fu_loca = intent_request["intent"]["slots"]["location"]["value"]
        return get_GoOtherPla_response(fu_loca)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.FallbackIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])