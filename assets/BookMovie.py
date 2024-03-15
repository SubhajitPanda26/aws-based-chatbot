"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages bookings for ONLINE MOVIE TICKETS.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'BookUrMovie' template.
For instructions on how to set up and test a bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html
"""
import math
import json
import datetime
import time
import dateutil.parser
import os
import logging
import re


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---


def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.
    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None
       
def final(movie_name,theater_name,movie_date, movie_time,ticket_count,seat_type):
    msg = 'Thank You, Your booking is confirmed.\n' \
    'Summary of tickets:\n'\
    'Movie: ' + movie_name +' ' \
    '\nTheater: ' + theater_name +' ' \
    '\nDate: ' + str(movie_date) + ' '\
    '\nTime: ' +str(movie_time) + ' '\
    '\nTotal ticket: ' + str(ticket_count) +' ' \
    '\nTotal Amount: ' + str(total_price(ticket_count, seat_type)) +' ' \
    '\n\nThank you for booking with chatbot. '
    return msg

def total_price(ticket_count, seat_type):
    if seat_type.lower() == 'gold':
        return (ticket_count * 150)
    elif seat_type.lower() == 'platinum':
        return (ticket_count * 200)
    elif seat_type.lower() == 'royal':
        return (ticket_count * 300)


def isvalid_movie(movie):
    valid_movies = ['sonar kella','aparajito','kabuliwala']
    return movie.lower() in valid_movies
    
def isvalid_theater(theater_name):
    valid_theater = ['pvr','inox','cinepolis']
    return theater_name.lower() in valid_theater

def isvalid_seat(seat_type):
    valid_seat = ['gold','platinum','royal']
    return seat_type.lower() in valid_seat


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def validate_movie(slots):
    user_name = try_ex(lambda: slots['UserName'])
    movie_name = try_ex(lambda: slots['MovieName'])
    theater_name = try_ex(lambda: slots['Theatre'])
    movie_date = try_ex(lambda: slots['Date'])
    movie_time = try_ex(lambda: slots['Time'])
    seat_type = try_ex(lambda: slots['SeatType'])
    ticket_count = safe_int(try_ex(lambda: slots['TicketNum']))


    if movie_date:
        if not isvalid_date(movie_date):
            return build_validation_result(False, 'Date', 'Sorry, I Am Unable to Understand. In Which Date You Want To Book The Movie Tickets?')
        if datetime.datetime.strptime(movie_date, '%Y-%m-%d').date() <= datetime.date.today():
            return build_validation_result(False, 'Date', 'Sorry, I Can Only Schedule Bookings At Least One Day In Advance.  Can You Try A Different Date?')
        if datetime.datetime.strptime(movie_date, '%Y-%m-%d').date() >= datetime.date.today()+datetime.timedelta(days=15):
            return build_validation_result(False, 'Date', 'You Can Book Only Upto 15 Days In Advance. Can You Try A Date Between {} and {}?'.format(datetime.date.today(),datetime.date.today()+datetime.timedelta(days=15)))
    
    if movie_time is not None:
        if len(movie_time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'Time', None)
        hour, minute = movie_time.split(':')
        hour = safe_int(hour)
        minute = safe_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'Time', None)
        if hour < 9 or hour > 22:
            # Outside of business hours
            return build_validation_result(False, 'Time', 'Movie Theatres Are Opened Only From 9 AM to 10 PM. Can You Specify A Time Within That Time Range?')
    
    
    if ticket_count is not None and ticket_count < 1:
        return build_validation_result(
            False,
            'TicketNum',
            'You Have To Book Atleast One Ticket. How Many Tickets Would You Like To Book?'
        )
    if ticket_count is not None and ticket_count > 20:
        return build_validation_result(
            False,
            'TicketNum',
            'You Can Book Maximum 20 Tickets At Once. How Many Tickets Would You Like To Book?'
        )
        

    return {'isValid': True}


""" --- Functions that control the bot's behavior --- """


def book_movie(intent_request):
    """
    Performs dialog management and fulfillment for booking a movie.
    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """

    user_name = try_ex(lambda: intent_request['currentIntent']['slots']['UserName'])
    movie_name = try_ex(lambda: intent_request['currentIntent']['slots']['MovieName'])
    theater_name = try_ex(lambda: intent_request['currentIntent']['slots']['Theatre'])
    seat_type = try_ex(lambda: intent_request['currentIntent']['slots']['SeatType'])
    movie_date = try_ex(lambda: intent_request['currentIntent']['slots']['Date'])
    movie_time = try_ex(lambda: intent_request['currentIntent']['slots']['Time'])
    ticket_count = safe_int(try_ex(lambda: intent_request['currentIntent']['slots']['TicketNum']))
    confirmation_status = intent_request['currentIntent']['confirmationStatus']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'ReservationType': 'Movie',
        'UserName': user_name,
        'MovieName': movie_name,
        'TheaterName': theater_name,
        'Date': movie_date,
        'Time': movie_time,
        'SeatType': seat_type,
        'TicketNum': ticket_count,
    })

    session_attributes['currentReservation'] = reservation

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_movie(intent_request['currentIntent']['slots'])
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )
        if confirmation_status == 'Confirmed':
            
            return delegate(session_attributes, intent_request['currentIntent']['slots'])
        # Otherwise, let native DM rules determine how to elicit for slots and prompt for confirmation.  Pass price
        # back in sessionAttributes once it can be calculated; otherwise clear any setting from sessionAttributes.

        session_attributes['currentReservation'] = reservation
        return delegate(session_attributes, intent_request['currentIntent']['slots'])

    # Booking the Movie.  In a real application, this would likely involve a call to a backend service.
    logger.debug('BookMovie under={}'.format(reservation))

    try_ex(lambda: session_attributes.pop('currentReservation'))
    session_attributes['lastConfirmedReservation'] = reservation

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': '{}'.format(final(movie_name,theater_name,movie_date, movie_time,ticket_count,seat_type))
                     
        }
    )

# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']
    # Dispatch to your bot's intent handlers
    if intent_name == 'BookMovie':
        return book_movie(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
