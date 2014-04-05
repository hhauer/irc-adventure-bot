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
        return ["Your password has been set."]
    except PasswordAlreadySetException:
        return ["You already have a password set."]

def do_change_password(listener, engine, user, tokens):
    verify_parameters(tokens, 2, "change_password <old_password> <new_password>")

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

    try:
        user.verify_password(tokens[0])
        return ["You are now authenticated."]
    except PasswordIncorrectException:
        return ["I was not able to validate your password."]

def do_markov(listener, engine, user, tokens):
    markov = engine.markov.generate()
    logger.debug("{} generated a markov chain: {}".format(user.username, markov))
    return markov

