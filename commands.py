from user import *

# Logging
import logging
logger = logging.getLogger(__name__)

class InvalidParametersException(Exception):
    pass

def verify_parameters(tokens, expected_count, format_text):
    if len(tokens) is not expected_count:
        raise InvalidParametersException(format_text)

def do_test(listener, engine, user, tokens):
    return ["Test succesful."]

def do_set_password(listener, engine, user, tokens):
    verify_parameters(tokens, 1, "set_password <password>")

    try:
        user.set_password(tokens[0])
        return ["Your password has been set. You are now registered."]
    except PasswordAlreadySetException:
        return ["You already have a password set."]

def do_change_password(listener, engine, user, tokens):
    verify_parameters(tokens, 2, "change_password <old_password> <new_password>")

    if user.auth is False:
        return "You must first authenticate before you may change your password."

    try:
        user.change_password(tokens[0], tokens[1])
        return ["Your password has been changed succesfully."]
    except PasswordChangeFailureException as e:
        logger.debug("Failure changing password for {}, exception: {}".format(user.username, e))
        return ["There was an error changing your password. Did you have one set?"]
    except PasswordIncorrectException:
        return ["I was not able to validate your old password."]

def do_authenticate(listener, engine, user, tokens):
    verify_parameters(tokens, 1, "authenticate <password>")

    if user.auth is True:
        return "You are already authenticated."

    try:
        user.verify_password(tokens[0])
        user.auth = True
        return ["You are now authenticated."]
    except PasswordIncorrectException:
        return ["I was not able to validate your password."]

def do_markov(listener, engine, user, tokens):
    markov = engine.markov.generate()
    logger.debug("{} generated a markov chain: {}".format(user.username, markov))
    return markov

def do_changelog(listener, engine, user, tokens):
    change = None
    with open('changelog.txt', 'r') as f:
        change = [l for l in f]

    return change

def do_help(listener, engine, user, tokens):
    output = None
    if len(tokens) is 0:
        with open('help/help.txt', 'r') as f:
            output = [l for l in f]
    else:
        try:
            helpfile = 'help/' + tokens[0]
            logger.debug("Trying to open helpfile: %s", helpfile)
            output = [l for l in f]
        except e:
            logger.debug("Exception loading help: {}".format(e))
            output = "That helpfile was not found."

    return output

def do_adventure(listener, engine, user, tokens):
    if len(tokens) is 0:
        return ["Please select a location to adventure:"] + [l for l in engine.zones.keys()]

    try:
        (level, mob) = engine.zones[tokens[0]].pick_mob()
        return "You encounter a level {} monster! The {} snarls menacingly.".format(level, mob)
    except KeyError:
        return "That is not a valid destination to adventure in."
