from __future__ import print_function
import requests
import ujson
import os
import webcolors

apiurl = 'https://api.particle.io/v1/devices'

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            #'type': 'PlainText',
            'type': 'SSML',
            #'text': output
            'ssml': '<speak>' + output + '</speak>'
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

# Basic function to fetch and parse
def fetchResults(url, args=None):

    if args is not None:
        data = {'access_token': os.environ['particleToken'], 'args': args}
    else:
        data = {'access_token': os.environ['particleToken']}
    try:
        response = requests.post(url, data = data)
        response = ujson.loads(response.text)
    except:
        response = None

    return response

def turnOn():
    url = "%s/%s/On" % (apiurl, os.environ['particleID'])
    print("Calling: %s" % url)
    results = fetchResults(url)
    print(results)
    if not results:
        response = "I'm sorry, something went wrong"
    else:
        try:
            response = results['error']
        except:
            response = "OK"

    speech_output = response
    reprompt_text = "Please try again"
    card_title = "Turn On"
    session_attributes = {}
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def setColour(colour):
    url = "%s/%s/setColour" % (apiurl, os.environ['particleID'])
    results = fetchResults(url, args=colour)
    if not results:
        response = "I'm sorry, something went wrong"
    else:
        try:
            response = results['error']
        except:
            response = "OK"

    speech_output = response
    reprompt_text = "Please try again"
    card_title = "Set Colour"
    session_attributes = {}
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def turnOff():
    url = "%s/%s/Off" % (apiurl, os.environ['particleID'])
    results = fetchResults(url)
    if not results:
        response = "I'm sorry, something went wrong"
    else:
        try:
            response = results['error']
        except:
            response = "OK"

    speech_output = response
    reprompt_text = "Please try again"
    card_title = "Turn Off"
    session_attributes = {}
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent)

    # Dispatch to your skill's intent handlers
    if intent_name == "turnOn":
        return turnOn()
    elif intent_name == "turnOff":
        return turnOff()
    elif intent_name == "setColour":
        colour = intent['slots']['colour']['value']
        colour = colour.replace(' ', '')
        try:
            colour = webcolors.name_to_hex(colour)
        except:
            raise ValueError("Couldn't grok colour")
        return setColour(colour)
    else:
        raise ValueError("Invalid intent")

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    #if (event['session']['application']['applicationId'] != "<APPLICATION_ID>"):
    #     raise ValueError("Invalid Application ID")


    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])